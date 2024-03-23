var map = L.map('map').setView([41.7647, -72.6828], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

// Function to fetch and add a GeoJSON layer with a specific icon
function addLayerFromGeoJSON(dataPath, iconName) {
  fetch(dataPath)
    .then(response => response.json())
    .then(data => {
      L.geoJSON(data, {
        pointToLayer: function(feature, latlng) {
          return L.marker(latlng, {
            icon: L.icon({
              iconUrl: `icons/${iconName}.png`,
              iconSize: [18, 18],
              iconAnchor: [8, 16],
              popupAnchor: [0, -16]
            })
          });
        }
      }).addTo(map);
    });
}

// Simplified getColor function
function getColor(gridcode) {
  if (gridcode >= 0 && gridcode <= 10) {
    return `hsl(${(gridcode / 10) * 120}, 100%, 50%)`;
  }
  return 'gray';
}

// Add Raster Overlay layer
fetch('data/RasterOverlay.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      style: function(feature) {
        return {
          fillColor: getColor(feature.properties.gridcode),
          fillOpacity: 0.7,
          color: getColor(feature.properties.gridcode),
          weight: 1
        };
      }
    }).addTo(map);
  });

// Adding layers for various features
addLayerFromGeoJSON('data/Brownfields.geojson', 'brownfield');
addLayerFromGeoJSON('data/Hospitals.geojson', 'hospital');
addLayerFromGeoJSON('data/Police Stations.geojson', 'police');
addLayerFromGeoJSON('data/Schools.geojson', 'school');

var legend = L.control.legend({
    position: 'bottomleft',
    legends: [{
      label: "Brownfields",
      type: "image",
      url: "icons/brownfield.png",
      layers: [/* layer reference */]
    }, {
      label: "Hospitals",
      type: "image",
      url: "icons/hospital.png",
      layers: [/* layer reference */]
    }, {
      label: "Police Stations",
      type: "image",
      url: "icons/police.png",
      layers: [/* layer reference */]
    }, {
      label: "Schools",
      type: "image",
      url: "icons/school.png",
      layers: [/* layer reference */]
    }
    ]
  }).addTo(map);

  
  
  