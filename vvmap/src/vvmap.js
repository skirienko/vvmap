import * as L from 'leaflet';
import '@maplibre/maplibre-gl-leaflet';
import mapstyleURL from './posi.json';
import streetsURL from './streets.geojson?url';

import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

const LEGEND = {
  'f': {color:'#FF3333', description: 'улицы в честь женщин'},
  'm': {color:'#3333FF', description: 'улицы в честь мужчин'},
  '-': {color:'#99AA99', description: 'нейтральные улицы'},
  '!': {color:'#CC33CC', description: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color:'#FFDD66', description: 'непонятно'}
}

const map = L.map('map', {attributionControl:false}).setView([43.103, 131.905], 12);

const gl = L.maplibreGL({
          // style: 'https://tiles.openfreemap.org/styles/positron'
          style: mapstyleURL,
          maxZoom: 19
        }).addTo(map);

const st = ({properties}) => {
  return {opacity:.75, color:getColor(properties.gender)}
}

fetch(streetsURL).then(r => r.json()).then(gj => {
  L.geoJSON(gj, {style:st}).addTo(map);
})

const legend = L.control();

legend.onAdd = function(map) {
  const ul = L.DomUtil.create('ul', 'legend');
  renderLegend(ul);
  return ul;
}
legend.addTo(map);

function renderLegend(el) {
  if (el) {
    Object.values(LEGEND).forEach(item => {
      const li = document.createElement('li');
      li.setAttribute('style', "color:"+item.color);
      li.appendChild(document.createTextNode(item.description));
      el.appendChild(li);
    });
  }
}

function getColor(key) {
  return key in LEGEND ? LEGEND[key].color : LEGEND['?'].color
}
