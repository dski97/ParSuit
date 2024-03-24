var map = L.map('map').setView([41.7647, -72.6828], 10);

// Custom pane for the raster overlay with higher z-index for mouse interaction
map.createPane('rasterPane');
map.getPane('rasterPane').style.zIndex = 450;

// Custom pane for parcels to ensure they are clickable, but below the raster layer
map.createPane('parcelPane');
map.getPane('parcelPane').style.zIndex = 400; // Make sure this is lower than rasterPane

//Gray layer
var Stadia_AlidadeSmooth = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.{ext}', {
	minZoom: 10,
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	ext: 'png'
});


// OSM layer
var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 19,
  minZoom: 10
});

//Satiellite layer
var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
  maxZoom: 19,
  minZoom: 10
});


//Add osmlayer to map
Stadia_AlidadeSmooth.addTo(map);

//Define base layers for toggling
var baseLayers = {
  "OSM": osmLayer,
  "Satellite": satelliteLayer,
  "Gray": Stadia_AlidadeSmooth
};

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
      },
      interactive: false // Disable interactivity
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

L.control.Legend ({
  position: "bottomleft",
  legends: [{
    label: "Brownfields",
    type: "image",
    url: "icons/brownfield.png",
  }, {
    label: "Hospitals",
    type: "image",
    url: "icons/hospital.png",
  }, {
    label: "Police Stations",
    type: "image",
    url: "icons/police.png",
  }, {
    label: "Schools",
    type: "image",
    url: "icons/school.png",
  },
  ]
}).addTo(map);

// Add the layer control to the map, including both base layers and overlay layers
L.control.layers(baseLayers, overlayLayers, {collapsed: false}).addTo(map);

// Define the main extent of the map
var mainExtent = {
  lat: 41.7647,
  lng: -72.6828,
  zoom: 10
};

// Create a custom control for returning to the main extent
L.Control.ReturnToExtent = L.Control.extend({
  options: {
    position: 'topleft', // Position of the control
  },

  onAdd: function (map) {
    // Create a button element
    var container = L.DomUtil.create('button', 'leaflet-bar leaflet-control leaflet-control-custom');
    container.innerHTML = 'Return to Main Extent'; // Text on the button
    container.style.backgroundColor = 'white';    
    container.style.width = 'auto';
    container.style.height = 'auto';
    container.style.padding = '5px';
    container.style.fontSize = '12px';
    container.style.cursor = 'pointer';

    // Prevent map clicks when clicking the control
    L.DomEvent.disableClickPropagation(container);

    // Set the map view to the main extent when the button is clicked
    L.DomEvent.on(container, 'click', function() {
      map.setView([mainExtent.lat, mainExtent.lng], mainExtent.zoom);
    });

    return container;
  }
});

// Add the custom control to the map
map.addControl(new L.Control.ReturnToExtent());