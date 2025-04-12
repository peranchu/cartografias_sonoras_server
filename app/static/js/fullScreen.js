/*
Manejo de la ruta FULLSCREEN.HTML
- Configuración del Mapa.
- Funciones de llamada a la Bd para pintar los marcadores en el Mapa
- Recepción y Envio a MAX por SOCKET
*/

//Llama a la función que carga las posiciones en el mapa al iniciar la vista
window.addEventListener("load", () => {
  DatosPosiciones();
});

var estado_repro = 0; // Estado del Reproductor de audio

//SOCKETS
const serverUrl = "http://localhost:5000"; //Server
const socket = io(serverUrl); //Librería para la comunicación socket con MAX

//Pinta los datos del mapa cada 10 ssegundos
//setInterval(() => DatosPosiciones(), 10000);

//----- CONFIGURACIÓN MAPA ------------
//Icono personalizado para marcador
var iconPers = L.icon({
  iconUrl: "/static/audioico.png",
});
//////////////////////

//Custom POPUPS, estilo para las ventana popup
var customOptions = {
  maxWidth: 400,
  width: 200,
  className: "popupCustom",
};
////////////////////

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
/////////////////////////

//Configura capas del mapa(Teselas....)
var SELF_Map = L.tileLayer("/static/img_maps/{z}/{x}/{y}.png", {
  minZoom: 14,
  maxZoom: 18,
  attribution: "&copy; OpenstreetMap",
}).addTo(map);
///////////////////////////////////////
// ------- FIN CONFIGURACIÓN MAPA ---------

// --- FUNCIONES LLAMADA A Db -----
//Llamada a la base de datos para pintar los marcadores en el mapa
async function DatosPosiciones() {
  await fetch("/api/posicionesMapa")
    .then((response) => response.json())
    .then((data) => {
      data.map((posiciones) => {
        const marker = L.marker([posiciones.latitude, posiciones.longitude], {
          draggable: true,
          icon: iconPers, //Icono personalizado
        }).addTo(map);

        marker.bindPopup(
          //marcadores contenido y botón
          `<p class="h6 text-dark fs-5 text-center">${posiciones.name}</p>` +
            `<p class="h6 text-dark fs-6 text-center">${posiciones.time}</p>` +
            `<p class="h6 text-dark fs-6 text-center">${posiciones.date}</p>` +
            //Archivo seleccionado para reproducir
            `<a class='btn btn-primary text-light btn-sm btn-center' onclick="mostrar(${posiciones.rowid});">Reproducir</a>`,

          customOptions // custom marker, estilos
        );
      });
    });
}
////////////////////////////////////

// si se esa reproduciendo deshabilita las reproduciones desde los marcadores
async function DatosPosiciones_repro() {
  await fetch("/api/posicionesMapa")
    .then((response) => response.json())
    .then((data) => {
      data.map((posiciones) => {
        const marker = L.marker([posiciones.latitude, posiciones.longitude], {
          draggable: true,
          icon: iconPers, //Icono personalizado
        }).addTo(map);
        marker.bindPopup(
          //marcadores contenido y botón
          `<p class="h6 text-dark fs-5 text-center">${posiciones.name}</p>` +
            `<p class="h6 text-dark fs-6 text-center">${posiciones.time}</p>` +
            `<p class="h6 text-dark fs-6 text-center">${posiciones.date}</p>` +
            //Archivo Reproduciendo
            `<a class='btn btn-primary disabled text-light btn-sm btn-center' onclick="">Reproduciendo</a>`,

          customOptions // custom marker, estilos
        );
      });
    });
}
///////////////////////////////////

//Función pide los datos del archivo a reproducir y lo pinta en pantalla, llamada desde los botones
// de los marcadores (DatosPosiciones)
async function mostrar(id) {
  // Si el reproductor esta Parado
  if (estado_repro == 0) {
    const url = "/api/repro/" + id;

    identificador = await fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const latitudeRepro = data[0].latitude;
        const longitudeRepro = data[0].longitude;

        // Pinta los campos en "fullScreen.html"
        document.getElementById("audio_name").innerHTML = data[0].audio_name;
        document.getElementById("name").innerHTML = data[0].name;
        document.getElementById("lat").innerHTML = data[0].latitude;
        document.getElementById("lon").innerHTML = data[0].longitude;
        document.getElementById("time").innerHTML = data[0].time;
        document.getElementById("date").innerHTML = data[0].date;

        // Centra y amplia el mapa en el punto de reproducción selecionado
        map.setView([latitudeRepro, longitudeRepro], 16);

        //Emite Socket
        //Envía el nombre de audio seleccionado al servidor para
        //ser enviado a MAX (socket.py)
        const nombre_audio = data[0].audio_name;
        socket.emit("repro_init", nombre_audio); // "socket.py"

        // Cambia el color de la cabezera "Reproduciendo"
        document.getElementById("header_card").classList.remove("bg-secondary"); //Elimina la clase del color rosado
        document.getElementById("header_card").classList.add("bg-primary"); //Añade la clase del color verde
        document.getElementById("header_card").innerHTML = "Reproduciendo"; // cambio texto cabezera

        estado_repro = 1;
      });

    // Descativa las funciones de reproducion desde los marcadores
    if (estado_repro == 1) {
      DatosPosiciones_repro();
    }
  }
}
////////////////////////////////////////
// --- FIN LLAMADAS A Db -----

// ---- SOCKETS -----
// Escucha los eventos socket que llegan de MAX atraves del Server
// Estado del reproductor de audio
// Parada de Audio  "socket.py"
socket.on("max_stop", (message) => {
  document.getElementById("header_card").classList.remove("bg-primary"); //Elimina la clase del color rosado
  document.getElementById("header_card").classList.add("bg-secondary"); //Añade la clase del color verde
  document.getElementById("header_card").innerHTML = "Stop"; // Cambio texto cabezera
  // Pinta los campos en "fullScreen.html"
  // Al Finalizar reproducción los vacía
  document.getElementById("audio_name").innerHTML = "";
  document.getElementById("name").innerHTML = "";
  document.getElementById("lat").innerHTML = "";
  document.getElementById("lon").innerHTML = "";
  document.getElementById("time").innerHTML = "";
  document.getElementById("date").innerHTML = "";

  //Activa las funciones del Mapa
  map.dragging.enable();
  map.touchZoom.enable();
  map.doubleClickZoom.enable();
  map.scrollWheelZoom.enable();
  map.boxZoom.enable();
  map.keyboard.enable();
  if (map.tap) map.tap.enable();
  document.getElementById("map").style.cursor = "grab";

  //Cierra todos los popup
  map.closePopup();

  // Centra y amplia el mapa en el punto Origen después de la reproducción
  map.setView([43.360870938239664, -5.5092986378873094], 14);

  estado_repro = 0;

  DatosPosiciones(); // Redibuja todos los marcadores
});

// En Reproduccion
socket.on("max_play", (message) => {
  //Cierra todos los popup
  map.closePopup();

  //Desactiva las funciones del mapa
  map.dragging.disable();
  map.touchZoom.disable();
  map.doubleClickZoom.disable();
  map.scrollWheelZoom.disable();
  map.boxZoom.disable();
  map.keyboard.disable();
  if (map.tap) map.tap.disable();
  document.getElementById("map").style.cursor = "default";
});
//////////////////////////////
// --- FIN SOCKETS ----
