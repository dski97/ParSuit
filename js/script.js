/**
 * Project: ParSuit WebViewer - A Web Mapping Application for Parcel Suitability Analysis
 * File Name: script.js
 * Description: This script initializes and configures a Leaflet map for displaying various 
 * geographic data layers, including schools, hospitals, police stations, and brownfields. 
 * It dynamically adds geoJSON layers, implements custom controls, and manages layer visibility 
 * based on zoom levels. Features include a custom legend, pane management for layer stacking, 
 * and interactive popups for detailed information.
 * 
 * Author: Dominic C
 */


// Set up the map
var map = L.map('map').setView([41.7647, -72.5828], 10);

//Glossary of terms
var glossary_terms = {
  'Away from Brownfields': 'Indicates the degree to which the land is inclined, affecting construction and drainage.',
  'Buildable Soil': 'Refers to soil with properties conducive to agriculture or construction.',
  'Away from Flood Zones': 'Areas less likely to experience flooding, reducing risk of water damage.',
  'Proximity to Hospitals': 'Distance from medical facilities, affecting emergency response times.',
  'Proximity to Police Stations': 'Distance from law enforcement, affecting crime rates and safety.',
  'Proximity to Roads': 'Distance from roads, affecting accessibility and noise pollution.',
  'Proximity to Schools': 'Distance from educational institutions, affecting property values and child safety.',
  'Public Sewer': 'Availability of immediate access to public sewer systems.',
  'Low Grade Slope': 'Indicates the degree to which the land is flat and suitable for construction.',
  'Away from Wetlands': 'Distance from wetlands, affecting environmental impact and land use.',
  'Appropriate Land Use': 'Refers to the suitability of the land for specific purposes such as residential, commercial, or industrial.'
};

// Variable to store the slider values
var slider_values = [];

// Function to fetch the slider values from the file
function fetchSliderValues() {
  // Return the fetch promise to the caller
  return fetch('slider_values.txt')
    .then(response => response.text())
    .then(data => {
      slider_values = data.split(',').map(Number);
      updateCombinedDataLegend(); // Assuming this function handles UI update
    })
    .catch(error => {
      console.error('Error fetching slider values:', error);
    });
}

// Function to combine glossary terms and slider values
function combineGlossaryAndSliderValues() {
  var combinedData = Object.entries(glossary_terms).reduce((result, [key, value], index) => {
    var term = key.split(':')[0].trim();
    var sliderValue = slider_values[index];
    result[term] = sliderValue;
    return result;
  }, {});
  return combinedData;
}

function updateCombinedDataLegend() {
  const combinedData = combineGlossaryAndSliderValues();
  let legendContent = '<h4>Weights</h4>'; // Optionally add a title

  for (const [term, value] of Object.entries(combinedData)) {
    legendContent += `<div class="legend-item"><span class="bold-term">${term}:</span> ${value}</div>`;
  }
  

  // Update the inner HTML of the custom legend
  document.getElementById('customLegend').innerHTML = legendContent;
}

// Example of updating the legend after fetching slider values
fetchSliderValues().then(() => {
  console.log('Slider values updated and legend refreshed.');
  // Any additional actions to take after updating slider values and refreshing the legend can go here
});


// Function to create and style panes
function createPane(name, zIndex) {
  map.createPane(name); // Create a pane with the given name
  map.getPane(name).style.zIndex = zIndex; // Set the z-index of the pane
}

createPane('rasterPane', 450); // Create a pane for the raster layer
createPane('parcelPane', 400); // Create a pane for the parcel layer

// Function to create a tile layer
function createTileLayer(url, attribution, minZoom = 10, maxZoom = 19, ext = 'png') { // Default values for minZoom, maxZoom, and ext
  return L.tileLayer(url, { attribution, minZoom, maxZoom, ext }); // Return a tile layer with the given URL, attribution, minZoom, maxZoom, and ext
}
// Stadia Alidade Smooth tile layer is added to the map
var Stadia_AlidadeSmooth = createTileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
  '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors');

// OSM, Satellite, and Gray tile layers are created
var osmLayer = createTileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors');

// Satellite tile layer is added to the map
var satelliteLayer = createTileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community');

//Stadia map open by default
Stadia_AlidadeSmooth.addTo(map);

// Base layers are created
var baseLayers = { "OSM": osmLayer, "Satellite": satelliteLayer, "Gray": Stadia_AlidadeSmooth };

// Geocoder control is added to the map
L.Control.geocoder({ position: 'topleft', defaultMarkGeocode: true }).addTo(map);

// Function to add a GeoJSON layer to the map
async function addLayerFromGeoJSON(dataPath, iconName) { // Function to add a GeoJSON layer to the map
  let response = await fetch(dataPath); // Fetch the data from the given path
  let data = await response.json(); // Get the JSON data from the response
  return L.geoJSON(data, { // Create a GeoJSON layer with the data
    pointToLayer: (feature, latlng) => L.marker(latlng, { icon: L.icon({ iconUrl: `icons/${iconName}.png`, iconSize: [20, 20], iconAnchor: [8, 16], popupAnchor: [0, -16] }) }) // Create a marker with the given icon
      .bindPopup(getPopupContent(iconName, feature)) // Bind a popup with the content returned by getPopupContent
  });
}

// Function to get the popup content based on the icon name and feature
function getPopupContent(iconName, feature) { // Function to get the popup content based on the icon name and feature
  const props = feature.properties; // Get the properties of the feature
  switch (iconName) { // Check the icon name
    case 'school': // If the icon name is 'school'
      return `<h3>${props.SchoolProg}</h3><p><strong>District:</strong> ${props.DistrictNa}</p><p><strong>Address:</strong> ${props.Line1Addr}</p>`;
    case 'police': // If the icon name is 'police'
      return `<h3>${props.NAME}</h3><p><strong>Address:</strong> ${props.ADDRESS}</p>`;
    case 'hospital': // If the icon name is 'hospital'
      return `<h3>${props.NAME}</h3><p><strong>Trauma Center Status:</strong> ${props.Trauma_Cen}</p>`;
    case 'brownfield': // If the icon name is 'brownfield'
      return `<h3>${props.Name}</h3>`;
    default: // If the icon name is not recognized
      return ''; // Default popup content if none matches
  }
}

// Function to get the color based on the gridcode
function getColor(gridcode) { // Function to get the color based on the gridcode
  return gridcode >= 0 && gridcode <= 10 ? `hsl(${(gridcode / 10) * 120}, 100%, 50%)` : 'gray'; // Return a color based on the gridcode
}

// Object to store the overlay layers
var overlayLayers = {};

// Function to add the raster layer to the map
async function addRasterLayer() { 
  const response = await fetch('data/RasterOverlay.geojson'); // Fetch the raster data
  const data = await response.json(); // Get the JSON data from the response
  return L.geoJSON(data, { // Create a GeoJSON layer with the data
    pane: 'rasterPane', // Add the layer to the 'rasterPane' pane
    style: feature => ({ // Style each feature based on its properties
      fillColor: getColor(feature.properties.gridcode), // Fill color based on the gridcode
      fillOpacity: 0.7, // Fill opacity
      color: getColor(feature.properties.gridcode), // Border color based on the gridcode
      weight: 1 // Border weight
    }),
    onEachFeature: (feature, layer) => { // Add event listeners to each feature
      layer.on('mouseover', () => updateInfoBox(feature.properties.gridcode)); // Update the info box on mouseover
      layer.on('mouseout', clearInfoBox); // Clear the info box on mouseout
    },
  }).addTo(map); // Add the layer to the map
}

// Feature layer is created
var featureLayer = L.esri.featureLayer({
  url: 'https://services.arcgis.com/HRPe58bUyBqyyiCt/arcgis/rest/services/ParcelsCRCOG/FeatureServer/0',
  pane: 'parcelPane', // Add the layer to the 'parcelPane' pane
  style: () => ({ // Style each feature
    color: '#000000', // Border color
    weight: 1, // Border weight
    opacity: 1, // Border opacity
    fillColor: 'gray', // Fill color
    fillOpacity: 0 // Fill opacity
  }),
  onEachFeature: (feature, layer) => { // Add event listeners to each feature
    var popupContent = `<h3>Location: ${feature.properties.LOCATION || ''}</h3>` +
                       `<p>Town Name: ${feature.properties.Town_Name || ''}</p>` +
                       `<p>Owner: ${feature.properties.OWNER || ''}</p>`;
    layer.bindPopup(popupContent); // Bind a popup with the content
  },
});

var zoomThreshold = 17; // Zoom threshold for showing the feature layer

// Function to update the visibility of the feature layer based on the zoom level
function updateFeatureLayerVisibility() { 
  var currentZoom = map.getZoom(); // Get the current zoom level
  if (currentZoom >= zoomThreshold) { // If the current zoom level is greater than or equal to the threshold
    if (!map.hasLayer(featureLayer)) { // If the map does not have the feature layer
      featureLayer.addTo(map); // Add the feature layer to the map
    }
  } else {
    if (map.hasLayer(featureLayer)) { // If the map has the feature layer
      map.removeLayer(featureLayer); // Remove the feature layer from the map
    }
  }
}

map.on('zoomend', updateFeatureLayerVisibility); // Update the visibility of the feature layer on zoomend
updateFeatureLayerVisibility(); // Update the visibility of the feature layer initially

// Loading multiple GeoJSON layers and the raster layer
(async () => {
  const layers = await Promise.all([ // Load multiple layers asynchronously
    addLayerFromGeoJSON('data/Brownfields.geojson', 'brownfield'), 
    addLayerFromGeoJSON('data/Hospitals.geojson', 'hospital'),
    addLayerFromGeoJSON('data/Police Stations.geojson', 'police'),
    addLayerFromGeoJSON('data/Schools.geojson', 'school'),
    addRasterLayer()
  ]);

  const layerNames = ["Brownfields", "Hospitals", "Police Stations", "Schools", "Suitability Raster"]; // Names of the layers
  layerNames.forEach((name, index) => overlayLayers[name] = layers[index]); // Add the layers to the overlayLayers object

  overlayLayers["Parcels"] = featureLayer; // Add the feature layer to the overlayLayers object

  L.control.layers(baseLayers, overlayLayers, {collapsed: false}).addTo(map); // Add the layers control to the map
})();

// Boundary layer is added to the map
(async () => {
  const response = await fetch('data/Boundary.geojson'); // Fetch the boundary data
  const data = await response.json(); // Get the JSON data from the response
  L.geoJSON(data, { // Create a GeoJSON layer with the data
    style: {
      color: '#000000', // Border color
      weight: 10, // Border weight
      fillOpacity: 0 // Fill opacity
    },
    interactive: false // Disable interactivity
  }).addTo(map);
})();

// Function to update the info box with the gridcode
function updateInfoBox(gridcode) { // Function to update the info box with the gridcode
  var infoBox = document.getElementById('info-box'); // Get the info box element
  if (infoBox) { // If the info box element exists
    infoBox.innerHTML = `Suitability Score: ${gridcode}`; // Update the content with the gridcode
    infoBox.style.backgroundColor = getColor(gridcode); // Update the background color based on the gridcode
    infoBox.style.display = 'block'; // Display the info box
  }
}

// Function to clear the info box
function clearInfoBox() {  // Function to clear the info box
  var infoBox = document.getElementById('info-box'); // Get the info box element
  if (infoBox) { // If the info box element exists
    infoBox.innerHTML = 'Hover over a raster cell'; // Update the content
    infoBox.style.backgroundColor = 'white'; // Reset the background color
  }
}

// Custom control for returning to the main extent
class ReturnToExtentControl extends L.Control { // Custom control for returning to the main extent
  constructor(options = {}) { // Constructor with default options
    super(options); // Call the super constructor
  }

  // Method to add the control to the map
  onAdd(map) { 
    var container = L.DomUtil.create('button', 'leaflet-bar leaflet-control leaflet-control-custom'); // Create a button element
    container.innerHTML = 'Return to Main Extent'; // Set the button text
    container.style.backgroundColor = 'white'; // Set the background color
    container.style.width = 'auto'; // Set the width
    container.style.height = 'auto'; // Set the height
    container.style.padding = '5px'; // Set the padding
    container.style.fontSize = '12px'; // Set the font size
    container.style.cursor = 'pointer'; // Set the cursor to pointer
    L.DomEvent.disableClickPropagation(container); // Disable click propagation
    L.DomEvent.on(container, 'click', () => { // Add a click event listener
      map.setView([41.7647, -72.5828], 10); // Return to the main extent
    });
    return container; // Return the container
  }
}

// ReturnToExtentControl is added to the map
map.addControl(new ReturnToExtentControl({ position: 'topleft' })); // Add the custom control to the map

// Legend control is added to the map
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