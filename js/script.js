// script.js
var map = L.map('map').setView([41.7647, -72.6828], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

fetch('data/RasterOverlay.geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: function(feature) {
                var gridcode = feature.properties.gridcode;
                var color = getColor(gridcode);
                return {
                    fillColor: color,
                    fillOpacity: 0.7,
                    color: color,
                    weight: 1
                };
            }
        }).addTo(map);
    });

function getColor(gridcode) {
    if (gridcode >= 0 && gridcode <= 10) {
        var hue = (gridcode / 10) * 120; // Convert gridcode to hue (0-120)
        return `hsl(${hue}, 100%, 50%)`;
    }
    return 'gray'; // Default color for gridcode outside the range
}