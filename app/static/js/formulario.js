//Accede a los campos del formulario vista
let lat_v = document.getElementById("lat_v");
let lng_v = document.getElementById("lng_v");

//Accede a los campos del formulario
let lat = document.getElementById("lat");
let lng = document.getElementById("lng");

// Cambia el cursor a cruz
document.getElementById("map").style.cursor = "crosshair";

//Configura los Bordes del mapa
var surEste = L.latLng(43.2932, -5.4052),
  norEste = L.latLng(43.405, -5.6029),
  bounds = L.latLngBounds(surEste, norEste);

var map = L.map("map", {
  maxBounds: bounds, //Bordes del mapa
  zoomControl: false,
  center: [43.360870938239664, -5.5092986378873094],
  zoom: 14,
});

//Configura capas del mapa(Teselas....)
var SELF_Map = L.tileLayer("/static/img_maps/{z}/{x}/{y}.png", {
  minZoom: 14,
  maxZoom: 18,
  attribution: "&copy; OpenstreetMap",
}).addTo(map);

//Eventos del MAPA
function onMaplClick(e) {
  //console.log("Posicion: " + e.latlng);
  selectPlace = e.latlng;
  console.log(selectPlace);
  lat.value = selectPlace.lat;
  lng.value = selectPlace.lng;

  lat_v.value = selectPlace.lat;
  lng_v.value = selectPlace.lng;
}

map.on("click", onMaplClick);

//Barra de Progreso subida
function update() {
  var element = document.getElementById("myProgressBar");
  var width = 1;
  var identity = setInterval(scene, 10);
  function scene() {
    if (width >= 100) {
      clearInterval(identity);
    } else {
      width++;
      element.style.width = width + "%";
    }
  }
}
