var map = L.map('map').setView([41.7647, -72.6828], 10);

// Custom pane for the raster overlay with higher z-index for mouse interaction
map.createPane('rasterPane');
map.getPane('rasterPane').style.zIndex = 450;

// Custom pane for parcels to ensure they are clickable, but below the raster layer
map.createPane('parcelPane');
map.getPane('parcelPane').style.zIndex = 400; // Make sure this is lower than rasterPane



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

var rasterLayerObj;

var rasterLayer = fetch('data/RasterOverlay.geojson')
  .then(response => response.json())
  .then(data => {
    return L.geoJSON(data, {
      pane: 'rasterPane',
      style: function(feature) {
        return {
          fillColor: getColor(feature.properties.gridcode),
          fillOpacity: 0.6,
          color: getColor(feature.properties.gridcode),
          weight: 1
        };
      },
      onEachFeature: function(feature, layer) {
        layer.on('mouseover', function(e) {
          var gridcode = feature.properties.gridcode;
          updateInfoBox(gridcode);
        });
        layer.on('mouseout', function(e) {
          clearInfoBox();
        });
      },
    });
  });

// Create a feature layer for the parcels
  var featureLayer = L.esri.featureLayer({
    url: 'https://services.arcgis.com/HRPe58bUyBqyyiCt/arcgis/rest/services/ParcelsCRCOG/FeatureServer/0',
    pane: 'parcelPane',
    style: function() {
      return {
        color: '#000000', // Border color
        weight: 1, // Border weight
        opacity: 1, // Border opacity
        fillColor: 'gray', // Fill color as gray
        fillOpacity: 0 // Lower the fill opacity
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
    },
  });
  
  // Create a custom pane for the parcel layer
  map.createPane('parcelPane');
  map.getPane('parcelPane').style.zIndex = 300;


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
  overlayLayers["Brownfields"] = layers[0];
  overlayLayers["Hospitals"] = layers[1];
  overlayLayers["Police Stations"] = layers[2];
  overlayLayers["Schools"] = layers[3];
  overlayLayers["Suitability Raster"] = layers[4].addTo(map);
  overlayLayers["Parcels"] = featureLayer;

  // Add the layer control to the map
  L.control.layers({}, overlayLayers, {collapsed: false}).addTo(map);
});

// Load and add the boundary layer with dark black outline and no fill
fetch('data/Boundary.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      // Style for the boundary
      style: {
        color: '#000000', // Dark black
        weight: 10, // Thickness of the line
        fillOpacity: 0 // No fill
      }
    }).addTo(map); // Add to the map without event listeners
  });


function updateInfoBox(gridcode) {
  var infoBox = document.getElementById('info-box');
  var scoreElement = document.getElementById('score');
  
  if (infoBox && scoreElement) {
    scoreElement.textContent = gridcode;
    infoBox.style.backgroundColor = getColor(gridcode);
    infoBox.style.display = 'block';
  }
}

function clearInfoBox() {
  var infoBox = document.getElementById('info-box');
  var scoreElement = document.getElementById('score');
  
  if (infoBox && scoreElement) {
    scoreElement.textContent = '-';
    infoBox.style.backgroundColor = 'white';
  }
}