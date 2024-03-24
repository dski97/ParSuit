var map = L.map('map').setView([41.7647, -72.6828], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 19,
  minZoom: 10
}).addTo(map);

// Add the geocoder control to the map
L.Control.geocoder({
    position: 'topleft',
    defaultMarkGeocode: true
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

// Add the feature service layer with minZoom option
var featureLayer = L.esri.featureLayer({
    url: 'https://services.arcgis.com/HRPe58bUyBqyyiCt/arcgis/rest/services/ParcelsCRCOG/FeatureServer/0',
    onEachFeature: function(feature, layer) {
      // Check if the feature has properties and the required properties are present
      if (feature.properties) {
        // Initialize the popup content string
        var popupContent = '';
        
        // Check and add LOCATION
        if (feature.properties.LOCATION) {
          popupContent += '<h3>Location: ' + feature.properties.LOCATION + '</p>';
        }
        
        // Check and add Town_Name
        if (feature.properties.Town_Name) {
          popupContent += '<p>Town Name: ' + feature.properties.Town_Name + '</p>';
        }
        
        // Check and add Owner
        if (feature.properties.OWNER) {
          popupContent += '<p>Owner: ' + feature.properties.OWNER + '</p>';
        }
  
        // Bind the constructed popup content to the current layer
        layer.bindPopup(popupContent);
      }
    }
  }).addTo(map);

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
  }]
}).addTo(map);

// Function to check and update the feature layer based on the current zoom level
function updateFeatureLayerVisibility() {
    var currentZoom = map.getZoom();
    if (currentZoom >= 16) {
      if (!map.hasLayer(featureLayer)) {
        map.addLayer(featureLayer); // Add the feature layer if the zoom level is 13 or higher and it's not already added
      }
    } else {
      if (map.hasLayer(featureLayer)) {
        map.removeLayer(featureLayer); // Remove the feature layer if the zoom level is less than 13
      }
    }
  }
  
  // Listen for zoom end events to show/hide the feature service layer based on zoom level
  map.on('zoomend', updateFeatureLayerVisibility);
  
  // Initial check to set the correct visibility of the feature service layer
  updateFeatureLayerVisibility();

  