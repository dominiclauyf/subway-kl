const COORDINATE_KUALA_LUMPUR = [3.13, 101.6841];
var map = L.map("map").setView(COORDINATE_KUALA_LUMPUR, 12);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

var currentMarkerCoordinate = null;
var currentMarker = null;
var circle = null;
var circleCoordinates = null;
var circleMarkers = null;

function cleanMap() {
  if (currentMarker !== null) {
    map.removeLayer(currentMarker);
    currentMarker = null;
  }
  if (circle !== null) {
    toogleCircle();
  }
}

function showCurrentMarker(lat, long) {
  if (currentMarker !== null) {
    // Same position do nothing
    if (
      JSON.stringify([lat, long]) === JSON.stringify(currentMarkerCoordinate)
    ) {
      return;
    }
    // remove old marker
    map.removeLayer(currentMarker);
  }

  currentMarkerCoordinate = [lat, long];

  map.setView(currentMarkerCoordinate, 12);
  currentMarker = L.marker(currentMarkerCoordinate).addTo(map);

  // If circle exist clear circle old data and toggle again based on new currentMarkerCoordinate
  if (circle !== null) {
    toogleCircle();
    toogleCircle();
  }
}

function getCoordinateInCircle() {
  var filteredCoordinateData = [];
  for (const d of data) {
    var coordinate = [d.lat, d.long];
    if (isInsideCircle(coordinate)) {
      filteredCoordinateData.push(coordinate);
    }
  }
  return filteredCoordinateData;
}

function showMarkerInCircle() {
  circleMarkers = [];
  circleCoordinates.forEach((coordinate) => {
    circleMarkers.push(L.marker(coordinate, { opacity: 0.4 }).addTo(map));
  });
}

function removeMarkerInCircle() {
  circleMarkers.forEach((marker) => {
    map.removeLayer(marker);
  });
  circleCoordinates = null;
  circleMarkers = null;
}

function toogleCircle() {
  if (currentMarkerCoordinate === null) {
    var myModal = new bootstrap.Modal(document.getElementById("myModal"));
    myModal.show();
    return;
  }
  if (circle === null) {
    circle = L.circle(currentMarkerCoordinate, {
      color: "red",
      fillColor: "#f03",
      fillOpacity: 0.1,
      radius: 5000,
    }).addTo(map);

    setTimeout(function () {
      circleCoordinates = getCoordinateInCircle();
      showMarkerInCircle();
    }, 100);
  } else {
    map.removeLayer(circle);
    removeMarkerInCircle();
    circle = null;
  }
}

function isInsideCircle(latlng) {
  var distance = circle.getLatLng().distanceTo(latlng);
  return distance <= circle.getRadius();
}
