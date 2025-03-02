import * as L from 'leaflet';
import maplibregl from 'maplibre-gl';
import '@maplibre/maplibre-gl-leaflet';

import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

const LEGEND = {
  'f': {color:'#FF3333', descr: 'улицы в честь женщин'},
  'm': {color:'#3333FF', descr: 'улицы в честь мужчин'},
  '-': {color:'#99AA99', descr: 'нейтральные улица'},
  '!': {color:'#CC33CC', descr: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color:'#FFDD66', descr: 'непонятно'}
}

console.log("Hi!")
console.log(L)
console.log(maplibregl)

const map = L.map('map', {attributionControl:false}).setView([43.103, 131.905], 12);

var gl = L.maplibreGL({
          // style: 'https://tiles.openfreemap.org/styles/positron'
          style: './posi.json',
          maxZoom: 19
        }).addTo(map);

fetch('./streets.json').then(r => r.json()).then(data => drawStreets(data));

const legend = L.control();

legend.onAdd = function(map) {
  const ul = L.DomUtil.create('ul', 'legend');
  renderLegend(ul);
  return ul;
}
legend.addTo(map);

function drawStreets(data) {
    Object.keys(data).forEach(k => {
      const color = getColor(data[k]['gender'])
      data[k]['parts'].forEach(part => {
        const kal = L.polyline(part, {color:color,opacity:.75}).addTo(map);
      });
    });
}

function renderLegend(leg) {
  if (leg) {
    Object.values(LEGEND).forEach(item => {
      const li = document.createElement('li');
      li.setAttribute('style', "color:"+item.color);
      li.appendChild(document.createTextNode(item.descr));
      leg.appendChild(li);
    });
  }
}

function getColor(key) {
  return key in LEGEND ? LEGEND[key].color : LEGEND['?'].color
}
