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

// Function to fetch and return a GeoJSON layer with a specific icon, and add popups based on layer type
async function addLayerFromGeoJSON(dataPath, iconName) {
  let response = await fetch(dataPath);
  let data = await response.json();
  return L.geoJSON(data, {
    pointToLayer: function(feature, latlng) {
      let marker = L.marker(latlng, {
        icon: L.icon({
          iconUrl: `icons/${iconName}.png`,
          iconSize: [19, 19],
          iconAnchor: [8, 16],
          popupAnchor: [0, -16]
        })
      });

      // Bind popups with specific fields based on the iconName (layer type)
      if(iconName === 'school') {
        let popupContent = `<h3>${feature.properties.SchoolProg}</h3>
                            <p><strong>District:</strong> ${feature.properties.DistrictNa}</p>
                            <p><strong>Address:</strong> ${feature.properties.Line1Addr}</p>`;
        marker.bindPopup(popupContent);
      } else if(iconName === 'police') {
        let popupContent = `<h3>${feature.properties.NAME}</h3>
                            <p><strong>Address:</strong> ${feature.properties.ADDRESS}</p>`;
        marker.bindPopup(popupContent);
      } else if(iconName === 'hospital') {
        let popupContent = `<h3>${feature.properties.NAME}</h3>
                            <p><strong>Trauma Center Status:</strong> ${feature.properties.Trauma_Cen}</p>`;
        marker.bindPopup(popupContent);
      } else if(iconName === 'brownfield') {
        let popupContent = `<h3>${feature.properties.Name}</h3>`;
        marker.bindPopup(popupContent);
      }

      return marker;
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
  style: function() {
    return {
      color: '#000000', // Border color
      weight: 1, // Border weight
      opacity: 1, // Border opacity
      fillColor: 'gray', // Fill color as gray
      fillOpacity: 0.05 // Lower the fill opacity
    };
  },
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
// Define the zoom level threshold
var zoomThreshold = 17;

// Function to check and update the visibility of the Feature Layer based on the current zoom level
function updateFeatureLayerVisibility() {
    var currentZoom = map.getZoom();
    if (currentZoom >= zoomThreshold) {
        if (!map.hasLayer(featureLayer)) {
            featureLayer.addTo(map);
        }
    } else {
        if (map.hasLayer(featureLayer)) {
            map.removeLayer(featureLayer);
        }
    }
}

// Listen for the zoomend event on the map
map.on('zoomend', function() {
    updateFeatureLayerVisibility();
});

// Initial check to set the correct visibility when the map is first loaded
updateFeatureLayerVisibility();

// Add layers for various features
Promise.all([
  addLayerFromGeoJSON('data/Brownfields.geojson', 'brownfield'),
  addLayerFromGeoJSON('data/Hospitals.geojson', 'hospital'),
  addLayerFromGeoJSON('data/Police Stations.geojson', 'police'),
  addLayerFromGeoJSON('data/Schools.geojson', 'school'),
  rasterLayer
]).then(layers => {
  overlayLayers["Brownfields"] = layers[0]; // Removed .addTo(map)
  overlayLayers["Hospitals"] = layers[1]; // Removed .addTo(map)
  overlayLayers["Police Stations"] = layers[2]; // Removed .addTo(map)
  overlayLayers["Schools"] = layers[3]; // Removed .addTo(map)
  overlayLayers["Suitability Raster"] = layers[4].addTo(map); // Raster Overlay can remain visible by default or remove .addTo(map) to hide it initially
  overlayLayers["Parcels"] = featureLayer; // Removed .addTo(map) to keep featureLayer off initially, if desired

  // Add the layer control to the map
  L.control.layers({}, overlayLayers, {collapsed: false}).addTo(map);
});