// import {map} from "leaflet";

// const osm = "https://www.openstreetmap.org/copyright";
// const copy = `© <a href='${osm}'>OpenStreetMap</a>`;
// const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
// const layer = L.tileLayer(url, { attribution: copy });
// const map = L.map("map", { layers: [layer] });

import * as L from "leaflet"

let map = L.map('map').setView([30,160],13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
  maxZoom:19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
