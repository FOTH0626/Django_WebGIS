import * as L from "leaflet";

// 初始化地图
let map = L.map("map").setView([32.916, 119.368], 8);

// 添加底图
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// 定义图层变量
let geoJsonLayer: L.GeoJSON | null = null;
let diffmapLayer: L.ImageOverlay | null = null;
let soliddiffmapLayer: L.ImageOverlay | null = null;
let originalImageLayer: L.ImageOverlay | null = null;

// 添加复选框的容器
//@ts-ignore
const controlContainer = L.control({ position: "topright" });

controlContainer.onAdd = () => {
  // 创建容器
  const container = L.DomUtil.create("div", "layer-control");

  // 添加内容
  container.innerHTML = `
    <label><input type="checkbox" id="toggle-geojson" > Show GeoJSON</label><br>
    <label><input type="checkbox" id="toggle-diffmap" > Show diffmap</label><br>
    <label><input type="checkbox" id="toggle-solid-diffmap"> Show Solid diffmap</label><br>
    <label><input type="checkbox" id="toggle-original" > Show Original Image</label>
  `;

  return container;
};

controlContainer.addTo(map);

// 加载 GeoJSON
fetch("./api/geojson/9")
  .then((response) => response.json())
  .then((data) => {
    geoJsonLayer = L.geoJSON(data.features, {
      style: {
        color: '#00f', // 边界颜色（蓝色）
        weight: 1.5, // 边界宽度
        opacity: 1, // 边界透明度
        fillOpacity: 0.2, // 填充透明度
        fillColor: '#00f', // 填充颜色
      },
    });
  })
  .catch((error) => console.error("Error loading GeoJSON:", error));

const file_url = '2'; // 图片文件编号

// 加载影像数据
async function loadImages() {
  try {
    // 获取经纬度范围
    const response = await fetch(`./api/image/coordinates/${file_url}`);
    const data = await response.json();

    if (response.ok) {
      const bounds = L.latLngBounds(
        [data.southwest.lat, data.southwest.lng],
        [data.northeast.lat, data.northeast.lng]
      );

      // 原始影像层
      originalImageLayer = L.imageOverlay(`./api/image/file/${file_url}`, bounds);

      // 热力图层
      diffmapLayer = L.imageOverlay(`./api/diffmap/${file_url}/3`, bounds);

      // 纯色热力图层
      soliddiffmapLayer = L.imageOverlay(`./api/binary_diffmap/${file_url}/3`, bounds);

      // 调整地图视图到图片范围
      map.fitBounds(bounds);
    } else {
      console.error("Failed to load coordinates:", data.error);
    }
  } catch (error) {
    console.error("Error loading image data:", error);
  }
}

loadImages();

// 添加复选框事件监听
document.addEventListener("change", (event) => {
  const target = event.target as HTMLInputElement;

  if (target.id === "toggle-geojson") {
    if (geoJsonLayer) {
      if (target.checked) {
        geoJsonLayer.addTo(map);
      } else {
        map.removeLayer(geoJsonLayer);
      }
    }
  } else if (target.id === "toggle-diffmap") {
    if (diffmapLayer) {
      if (target.checked) {
        diffmapLayer.addTo(map);
      } else {
        map.removeLayer(diffmapLayer);
      }
    }
  } else if (target.id === "toggle-solid-diffmap") {
    if (soliddiffmapLayer) {
      if (target.checked) {
        soliddiffmapLayer.addTo(map);
      } else {
        map.removeLayer(soliddiffmapLayer);
      }
    }
  } else if (target.id === "toggle-original") {
    if (originalImageLayer) {
      if (target.checked) {
        originalImageLayer.addTo(map);
      } else {
        map.removeLayer(originalImageLayer);
      }
    }
  }
});
