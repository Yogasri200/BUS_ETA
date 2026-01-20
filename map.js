alert("map.js loaded");

const dataDiv = document.getElementById("bus-data");
const buses = JSON.parse(dataDiv.dataset.buses);

const map = L.map("map").setView([28.6139, 77.2090], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

buses.forEach(bus => {
  if (bus.lat && bus.lon) {
    L.marker([bus.lat, bus.lon])
      .addTo(map)
      .bindPopup(
        `Bus: ${bus.bus_number}<br>
         ETA: ${bus.eta}<br>
         Seats: ${bus.seats}`
      );
  }
});
