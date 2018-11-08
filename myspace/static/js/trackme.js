// get position from browser
const latInput = document.getElementById('lat');
const lonInput = document.getElementById('lon');
const accuracy = document.getElementById('accuracy');

navigator.geolocation.getCurrentPosition((pos) => {
  latInput.value = pos.coords.latitude;
  lonInput.value = pos.coords.longitude;
  accuracy.value = pos.coords.accuracy;
});

// f03

// Users color selection (TEMPORARY FIX)
function getColor(user) {
  switch(user) {
    case 'giacomo':
      return '#f03';
    case 'test':
      return '#0f6';
    default:
      return '#000';
  }
}

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
          color: getColor(item.user),
          fillColor: getColor(item.user),
          fillOpacity: 0.5,
          radius: item.accuracy
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
getLocations('https://giacomoc.com/trackme/locations/api/v0.1', 1);

// handle selection buttons
const trackAll = document.getElementById('track-all');
const trackUser = document.getElementById('track-user');

if (trackAll && trackUser) {
  let currentUser = trackUser.getAttribute('data-user');

  trackAll.addEventListener('click', () => {
    getLocations('https://giacomoc.com/trackme/locations/api/v0.1', 1);
    trackAll.style.fontWeight = 'bold';
    trackUser.style.fontWeight = "normal";
  });

  trackUser.addEventListener('click', () => {
    getLocations('https://giacomoc.com/trackme/locations/api/v0.1?user=' + currentUser, 4);
    trackAll.style.fontWeight = 'normal';
    trackUser.style.fontWeight = 'bold';
  });
}
