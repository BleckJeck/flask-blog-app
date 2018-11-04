// get position from browser
const latInput = document.getElementById('lat');
const lonInput = document.getElementById('lon');

navigator.geolocation.getCurrentPosition((pos) => {
  latInput.value = pos.coords.latitude;
  lonInput.value = pos.coords.longitude;
});

// initialize leaflet.js map
let mymap = L.map('map', {
  center: [0, 0],
  zoom: 1
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 20,
  id: 'mapbox.streets',
  accessToken: 'pk.eyJ1IjoiYmxlY2tqZWNrOTAiLCJhIjoiY2pvMnQ4Zjd0MDEzMjNsbjIzN280ZWU3diJ9.C_O3E6QyjZbKqDX_cNe0NQ'
}).addTo(mymap);

// used to handle different views
let circleGroup = new L.layerGroup().addTo(mymap);

// Fetch data and add markers
function getLocations(url, zoom) {

  fetch(url)
    .then(response => response.json())
    .then(data => {

      circleGroup.clearLayers();

      data.forEach(item => {
        let circle = L.circle([item.lat, item.lon], {
          color: 'red',
          fillColor: '#f03',
          fillOpacity: 0.5,
          radius: 500
        })

        if (item.place) {
          circle.bindTooltip(item.user + " @ " + item.place);
        } else {
          circle.bindTooltip(item.user + " was here!");
        }

        circleGroup.addLayer(circle);
      })

      // center map on latest location
      let latest = data[data.length - 1]
      mymap.setView([latest.lat, latest.lon], zoom);
    })
    .catch(err => console.log(err));
};

// get all users (standard view)
getLocations('http://localhost:5000/trackme/locations/api/v0.1', 1);

// handle selection buttons
const trackAll = document.getElementById('track-all');
const trackUser = document.getElementById('track-user');

if (trackUser && trackUser) {
  let currentUser = trackUser.getAttribute('data-user');

  trackAll.addEventListener('click', () => {
    getLocations('http://localhost:5000/trackme/locations/api/v0.1', 1);
    trackAll.style.fontWeight = 'bold';
    trackUser.style.fontWeight = "normal";
  });

  trackUser.addEventListener('click', () => {
    getLocations('http://localhost:5000/trackme/locations/api/v0.1?user=' + currentUser, 4);
    trackAll.style.fontWeight = 'normal';
    trackUser.style.fontWeight = 'bold';
  });
}