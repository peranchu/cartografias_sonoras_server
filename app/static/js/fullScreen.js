//Llama a la función que carga las posiciones en el mapa al iniciar la vista
window.addEventListener("load", () => {
  DatosPosiciones();
});

//SOCKETS
const socket = io();

//Pinta los datos del mapa cada 5 ssegundos
//setInterval(() => DatosPosiciones(), 10000);

//Configuración del mapa
var map = L.map("map", {
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

//Función pide los datos del archivo a reproducir y lo pinta en pantalla
async function mostrar(id) {
  const url = "/api/repro/" + id;

  identificador = await fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const latitudeRepro = data[0].latitude;
      const longitudeRepro = data[0].longitude;

      document.getElementById("audio_name").innerHTML = data[0].audio_name;
      document.getElementById("name").innerHTML = data[0].name;
      document.getElementById("lat").innerHTML = data[0].latitude;
      document.getElementById("lon").innerHTML = data[0].longitude;
      document.getElementById("time").innerHTML = data[0].time;
      document.getElementById("date").innerHTML = data[0].date;

      map.setView([latitudeRepro, longitudeRepro], 16);

      //Emite Socket
      //Envía el nombre de audio seleccionado al servidor para
      //ser enviado a MAX (socket.py)
      const nombre_audio = data[0].audio_name;
      socket.emit('repro_init', nombre_audio);
    });
}
///////////////

//Llamada a la base de datos para pintar los marcadores
async function DatosPosiciones() {
  await fetch("/api/posicionesMapa")
    .then((response) => response.json())
    .then((data) => {
      data.map((posiciones) => {
        const marker = L.marker([posiciones.latitude, posiciones.longitude], {
          draggable: true,
        }).addTo(map);
        marker.bindPopup(
          posiciones.name +
            "</br>" +
            posiciones.time +
            "</br>" +
            posiciones.date +
            "</br>" +
            posiciones.rowid +
            //Archivo seleccionado para reproducir
            `<br></br><a class='btn btn-info btn-sm' onclick="mostrar(${posiciones.rowid});">Reproducir</a>`
        );
      });
    });
}
