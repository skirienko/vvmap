import * as L from 'leaflet';
import maplibregl from 'maplibre-gl';
import '@maplibre/maplibre-gl-leaflet';

import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

console.log("Hi!")
console.log(L)
console.log(maplibregl)

var map = L.map('map', {attributionControl:false}).setView([43.103, 131.905], 12);

var gl = L.maplibreGL({
          // style: 'https://tiles.openfreemap.org/styles/positron'
          style: './posi.json',
          maxZoom: 19
        }).addTo(map);

fetch('./streets.json').then(r => r.json()).then(data => drawStreets(data));

function drawStreets(data) {
    Object.keys(data).forEach(k => {
      const color = getColor(data[k]['gender'])
      data[k]['parts'].forEach(part => {
        const kal = L.polyline(part, {color:color}).addTo(map);
      });
    });
}

const COLORS = {
  'f': 'red',
  'm': 'blue',
  '-': 'gray',
  '!': 'purple'
}

function getColor(key) {
  return key in COLORS ? COLORS[key] : 'yellow'
}
