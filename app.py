from flask import Flask, render_template, request
import requests
import pandas as pd
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import math
import random

app = Flask(__name__)

# ✅ Delhi Gov Real-Time Feed
REALTIME_URL = "https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key=Pz30tEVYZD5nDzOVBGRCxr4iniCDSS04"

# ✅ Load GTFS static data
stops_df = pd.read_csv("stops.txt")
routes_df = pd.read_csv("routes.txt")
trips_df = pd.read_csv("trips.txt")
stop_times_df = pd.read_csv("stop_times.txt")


# ---------------- Helper Functions ----------------
def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lon points."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def fetch_live_buses():
    """Fetch real-time vehicle positions from Delhi API."""
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        response = requests.get(REALTIME_URL, timeout=10)
        response.raise_for_status()
        feed.ParseFromString(response.content)
        data = MessageToDict(feed)
        return data.get("entity", [])
    except Exception as e:
        print("❌ Error fetching realtime feed:", e)
        return []


def get_route_info(route_id):
    """Fetch bus number & route details from GTFS."""
    route = routes_df[routes_df["route_id"] == route_id]
    if not route.empty:
        return route.iloc[0]["route_short_name"], route.iloc[0]["route_long_name"]
    return "Unknown", "Unknown"


# ---------------- Flask Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bus/<bus_id>")
def bus_seats(bus_id):
    """
    Show seat availability for a bus.
    Currently random availability, can be replaced with ML prediction.
    """
    seats = []
    for i in range(1, 41):  # Assume 40 seats
        status = random.choice(["available", "booked"])
        seats.append({"id": i, "status": status})

    return render_template("bus_seats.html", bus_id=bus_id, seats=seats)


@app.route("/search", methods=["POST"])
def search_buses():
    source = request.form["source"]
    destination = request.form["destination"]

    # ✅ Find matching stops
    source_stops = stops_df[stops_df["stop_name"].str.contains(source, case=False, na=False)]
    dest_stops = stops_df[stops_df["stop_name"].str.contains(destination, case=False, na=False)]

    if source_stops.empty or dest_stops.empty:
        return render_template("results.html", source=source, destination=destination, buses=[])

    source_stop = source_stops.iloc[0]
    dest_stop = dest_stops.iloc[0]

    source_stop_id = source_stop["stop_id"]
    dest_stop_id = dest_stop["stop_id"]

    # ✅ Trips covering source & destination
    trips_with_source = stop_times_df[stop_times_df["stop_id"] == source_stop_id]["trip_id"].unique()
    trips_with_dest = stop_times_df[stop_times_df["stop_id"] == dest_stop_id]["trip_id"].unique()
    valid_trips = set(trips_with_source).intersection(set(trips_with_dest))

    buses = []
    entities = fetch_live_buses()
    print("🔎 Live buses fetched:", len(entities))  # Debug

    for entity in entities:
        if "vehicle" not in entity:
            continue

        vehicle = entity["vehicle"]
        pos = vehicle.get("position", {})
        if not pos:
            continue

        trip_info = vehicle.get("trip", {})
        trip_id = trip_info.get("tripId")
        route_id = trip_info.get("routeId")

        bus_number, bus_name = get_route_info(route_id)
        license_plate = vehicle.get("vehicle", {}).get("label") or vehicle.get("vehicle", {}).get("id", "Not Available")

        lat = float(pos["latitude"])
        lon = float(pos["longitude"])

        # ✅ ETA calculation (to source stop)
        stop_lat = float(source_stop["stop_lat"])
        stop_lon = float(source_stop["stop_lon"])
        dist_km = haversine(lat, lon, stop_lat, stop_lon)
        eta = round((dist_km / 20) * 60, 1)  # avg 20 km/h

        # ✅ Match filtering
        if trip_id in valid_trips:
            match_type = "Exact Trip Match"
        elif route_id in list(trips_df[trips_df["trip_id"].isin(valid_trips)]["route_id"].unique()):
            match_type = "Route Match"
        elif dist_km <= 5:  # Nearby
            match_type = "Nearby Bus"
        else:
            continue

        # ✅ Seat load factor (random for now; later connect ML / live API)
        seat_factor = random.random()
        if seat_factor > 0.7:
            seat_status = "Low"      # Few seats left
        elif seat_factor > 0.4:
            seat_status = "Medium"   # Moderate
        else:
            seat_status = "High"     # Many available

        # ✅ Append bus info
        buses.append({
            "bus_number": bus_number,
            "bus_name": bus_name,
            "license_plate": license_plate,
            "lat": lat,
            "lon": lon,
            "eta": f"{eta} min",
            "match": match_type,
            "seats": seat_status
        })

    return render_template("results.html",
                           source=source,
                           destination=destination,
                           buses=buses)


if __name__ == "__main__":
    app.run(debug=True)
