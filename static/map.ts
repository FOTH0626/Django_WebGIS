import * as L from "leaflet";



let map = L.map('map').setView([32.916,119.368],8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
  maxZoom:19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

fetch('./api/geojson/9')
    .then(response => response.json())
    .then(data=>{
        let geoJson = data.features;
        L.geoJSON(geoJson).addTo(map);
    });


