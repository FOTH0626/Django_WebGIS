import * as L from "leaflet";


async function loadGeoJsonAndDisplayMap(id:number){
  try{
    let response = await fetch(`./api/geojson/${id}`);
    // let geojson = await response.json();
    const {features} = await response.json();
    const geojson = features[0];
    if (geojson) {
      // let features = geojson.features;
      // @ts-ignore
      console.log(geojson);
      L.geoJSON(geojson,{style:{color:'#ff00ff',weight:2}}).addTo(map);
    }
  }catch (e){
    console.error(e);
  }
}

let map = L.map('map').setView([32.916,119.368],8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
  maxZoom:19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
//
// let labelPane = map.createPane('labelPane');
// labelPane.style.zIndex = '600';
//
// let labelElement = document.getElementById('label');
//
// if (labelElement) {
//   labelPane.appendChild(labelElement);
//   labelElement.style.position = 'absolute';
//   labelElement.style.top = '15px';
//   labelElement.style.right = '15px';
// }else{
//   console.error('Label element not found');
// }

loadGeoJsonAndDisplayMap(1);


