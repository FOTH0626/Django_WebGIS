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


async function loadImage() {
  try {
    // 获取经纬度范围
    const response = await fetch("./api/image/coordinates/1");
    const data = await response.json();

    if (response.ok) {
      const bounds = L.latLngBounds(
        [data.southwest.lat, data.southwest.lng],
        [data.northeast.lat, data.northeast.lng]
      );

      // 添加图片覆盖层
      L.imageOverlay("./api/image/file/1", bounds).addTo(map);

      // 调整地图视图到图片范围
      map.fitBounds(bounds);
    } else {
      console.error("Failed to load coordinates:", data.error);
    }
  } catch (error) {
    console.error("Error loading image data:", error);
  }
}

loadImage();



