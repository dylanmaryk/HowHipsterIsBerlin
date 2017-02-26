var map = L.map("map").setView([52.52, 13.405], 10);

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZHlsYW5tYXJ5ayIsImEiOiJjaXo4eDM2ZDMwMDN3Mndud3Q0dDBzMTR4In0.p1Nm3ph7bEwn0Wypzw-BUA", {
  id: "mapbox.light",
  attribution: "&copy; <a href=\"https://www.mapbox.com/map-feedback/\">Mapbox</a> &copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> <strong><a href=\"https://www.mapbox.com/map-feedback/\" target=\"_blank\">Improve this map</a></strong>"
}).addTo(map);

var geoJSON = L.geoJson(polygonsPostcodesGeoJSON, {
  style: layerStyle,
  onEachFeature: onEachFeature
}).addTo(map);

function layerStyle(feature) {
    return {
        fillColor: postcodeAreaColor(feature.properties.venueCount),
        weight: 2,
        opacity: 1,
        color: "white",
        dashArray: "3",
        fillOpacity: 0.7
    };
}

function postcodeAreaColor(venueCount) {
    return venueCount > 100 ? "#800026" :
           venueCount > 50  ? "#BD0026" :
           venueCount > 20  ? "#E31A1C" :
           venueCount > 10  ? "#FC4E2A" :
           venueCount > 5   ? "#FD8D3C" :
           venueCount > 2   ? "#FEB24C" :
           venueCount > 1   ? "#FED976" :
                              "#FFEDA0";
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
    layer.bindPopup("Postcode: " + feature.properties.postcode + ", " +
                    "Number of cafes: " + feature.properties.venueCount);
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: "#666",
        dashArray: "",
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    geoJSON.resetStyle(e.target);
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}
