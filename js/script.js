var map = L.map('map').setView([41.7647, -72.6828], 10);

// Base layer
var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 19,
  minZoom: 10
}).addTo(map);

// Add the geocoder control to the map
L.Control.geocoder({
  position: 'topleft',
  defaultMarkGeocode: true
}).addTo(map);

// Function to fetch and return a GeoJSON layer with a specific icon
async function addLayerFromGeoJSON(dataPath, iconName) {
  let response = await fetch(dataPath);
  let data = await response.json();
  return L.geoJSON(data, {
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
  });
}

// Simplified getColor function
function getColor(gridcode) {
  if (gridcode >= 0 && gridcode <= 10) {
    return `hsl(${(gridcode / 10) * 120}, 100%, 50%)`;
  }
  return 'gray';
}

// Initialize overlay layers object for control
var overlayLayers = {};

// Add Raster Overlay layer
var rasterLayer = fetch('data/RasterOverlay.geojson')
  .then(response => response.json())
  .then(data => {
    return L.geoJSON(data, {
      style: function(feature) {
        return {
          fillColor: getColor(feature.properties.gridcode),
          fillOpacity: 0.7,
          color: getColor(feature.properties.gridcode),
          weight: 1
        };
      }
    });
  });

// Define and add the feature service layer
var featureLayer = L.esri.featureLayer({
  url: 'https://services.arcgis.com/HRPe58bUyBqyyiCt/arcgis/rest/services/ParcelsCRCOG/FeatureServer/0',
  onEachFeature: function(feature, layer) {
    var popupContent = '';
    if (feature.properties.LOCATION) {
      popupContent += '<h3>Location: ' + feature.properties.LOCATION + '</h3>';
    }
    if (feature.properties.Town_Name) {
      popupContent += '<p>Town Name: ' + feature.properties.Town_Name + '</p>';
    }
    if (feature.properties.OWNER) {
      popupContent += '<p>Owner: ' + feature.properties.OWNER + '</p>';
    }
    layer.bindPopup(popupContent);
  }
});

// Add layers for various features
Promise.all([
  addLayerFromGeoJSON('data/Brownfields.geojson', 'brownfield'),
  addLayerFromGeoJSON('data/Hospitals.geojson', 'hospital'),
  addLayerFromGeoJSON('data/Police Stations.geojson', 'police'),
  addLayerFromGeoJSON('data/Schools.geojson', 'school'),
  rasterLayer
]).then(layers => {
  overlayLayers["Brownfields"] = layers[0].addTo(map);
  overlayLayers["Hospitals"] = layers[1].addTo(map);
  overlayLayers["Police Stations"] = layers[2].addTo(map);
  overlayLayers["Schools"] = layers[3].addTo(map);
  overlayLayers["Raster Overlay"] = layers[4].addTo(map);

  overlayLayers["Feature Layer"] = featureLayer.addTo(map);

  // Add the layer control to the map
  L.control.layers({}, overlayLayers, {collapsed: false}).addTo(map);
});

// Unified function to control feature layer visibility based on zoom level
function controlFeatureLayerVisibility() {
    var currentZoom = map.getZoom();
    if (currentZoom >= 16) {
      if (!map.hasLayer(featureLayer)) {
        map.addLayer(featureLayer);
      }
    } else {
      if (map.hasLayer(featureLayer)) {
        map.removeLayer(featureLayer);
      }
    }
}

// Execute controlFeatureLayerVisibility after a slight delay to ensure map initialization
setTimeout(controlFeatureLayerVisibility, 100);

// Listen for zoom end events to control the feature service layer based on zoom level
map.on('zoomend', controlFeatureLayerVisibility);