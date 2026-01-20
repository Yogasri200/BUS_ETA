# 🚌 BUS ETA & Seat Availability System

This project is a **Real-Time Bus ETA and Seat Availability Prediction System** built using **Flask**, **GTFS static data**, and **GTFS real-time vehicle positions** from Delhi Open Transit Data.

It allows users to:
- Search buses between a **source stop** and **destination stop**
- View **estimated arrival time (ETA)**
- See **seat availability status**
- Visualize buses on a **map using Leaflet**
- View bus coordinates (latitude & longitude)

---

## 🚀 Features

- 🔍 Source → Destination bus search
- ⏱ Real-time ETA calculation
- 💺 Seat availability indicator (High / Medium / Low)
- 🗺 Live map with bus markers
- 📍 Latitude & Longitude display
- 🎟 Seat view button (UI ready)

---

## 🛠 Technologies Used

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, Bootstrap  
- **Mapping:** Leaflet.js, OpenStreetMap  
- **Data Source:** GTFS Static + GTFS Real-Time (Delhi Open Transit Data)

---

## 📂 Project Structure

BUS_ETA/
├── app.py
├── templates/
│ ├── index.html
│ ├── results.html
│ └── bus_seats.html
├── static/
│ └── js/
│ └── map.js
├── routes.txt
├── stops.txt
├── trips.txt
├── DATASET_NOTE.txt

---

## 📊 Dataset Information

This project uses **GTFS data provided by Delhi Open Transit Data**.

- `routes.txt`
- `stops.txt`
- `trips.txt`
- `stop_times.txt` ❌ (large file, not included in GitHub)

⚠️ **Note:**  
`stop_times.txt` is a large file (~140MB) and cannot be uploaded using GitHub web interface.  
Instructions to download and place this file locally are provided in `DATASET_NOTE.txt`.

---

## ▶️ How to Run the Project Locally

1. Install Python 
2. Download GTFS data from:
[Delhi Open Transit Data](https://otd.delhi.gov.in/)
3. Place `stop_times.txt` in the project root folder
4. Install required libraries:
```bash
pip install flask pandas requests protobuf gtfs-realtime-bindings
5.Run the application:
python app.py
6.Open browser and go to:
http://127.0.0.1:5000
