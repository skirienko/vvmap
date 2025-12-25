import * as L from 'leaflet';
import '@maplibre/maplibre-gl-leaflet';
import mapstyleURL from './posi.json';

import Gender from './Gender';
import Year from './Year';

import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';
/*
const routes = [
  { path: '/', callback: () => console.log('Home page') },
  { path: '/gender', callback: () => console.log('Gender') },
  { path: '/year', callback: () => console.log('Year') },
];
*/
const T = new Gender();

const map = L.map('map', {attributionControl:false}).setView([43.103, 131.905], 12);

const gl = L.maplibreGL({
          // style: 'https://tiles.openfreemap.org/styles/positron'
          style: mapstyleURL,
          maxZoom: 19
        }).addTo(map);

const st = ({properties}) => {
  return {opacity:.75, color:T.getColor(properties[T.topic])}
}

fetch(T.getURL()).then(r => r.json()).then(gj => {
  L.geoJSON(gj, {
    style: st,
    onEachFeature: createPopup,
  }).addTo(map);
})

const legend = L.control();

legend.onAdd = function(_map) {
  const ul = L.DomUtil.create('ul', 'legend');
  renderLegend(ul);
  return ul;
}
legend.addTo(map);

function renderLegend(el) {
  if (el) {
    Object.values(T.getLegend()).forEach(item => {
      const li = document.createElement('li');
      li.setAttribute('style', "color:"+item.color);
      li.appendChild(document.createTextNode(item.description));
      el.appendChild(li);
    });
  }
}

function createPopup(feature, layer) {
  layer.bindPopup(T.getText(feature.properties))
}