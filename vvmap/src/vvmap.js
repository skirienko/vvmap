import * as L from 'leaflet';
import '@maplibre/maplibre-gl-leaflet';
import mapstyleURL from './posi.json';
import Router from './Router';

import Gender from './Gender';
import Year from './Year';
import Type from './Type';

import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

let T;

const routes = [
  { path: '/gender', description: 'улицы по полу', callback: () => {T = new Gender() }},
  { path: '/year', description: 'улицы по годам', callback: () => { T = new Year() } },
  { path: '/type', description: 'улицы по типам', callback: () => { T = new Type() } },
];
const router = new Router(routes);

document.title = T.getTitle();

const map = L.map('map', {attributionControl:false}).setView([43.103, 131.905], 12);

L.maplibreGL({
          // style: 'https://tiles.openfreemap.org/styles/positron'
          style: mapstyleURL,
          maxZoom: 19
        }).addTo(map);

const styler = ({properties}) => {
  return {opacity:.75, color:T.getColor(properties[T.topic])}
}

fetch(T.getURL()).then(r => r.json()).then(gj => {
  L.geoJSON(gj, {
    style: styler,
    onEachFeature: createPopup,
  }).addTo(map);
})

const switcher = L.control();
switcher.onAdd = function(_map) {
  const select = L.DomUtil.create('select', 'switcher');
  renderSwitcher(select);
  return select;
}
switcher.addTo(map);

const legend = L.control();
legend.onAdd = function(_map) {
  const ul = L.DomUtil.create('ul', 'legend');
  renderLegend(ul);
  return ul;
}
legend.addTo(map);


function renderSwitcher(select) {
  routes.forEach(r => {
    const option = document.createElement('option');
    option.setAttribute('value', r.path);
    if (r === router.getCurrentRoute()) {
      option.setAttribute('selected', true);
    }
    option.appendChild(document.createTextNode(r.description));
    select.appendChild(option);
  });
  select.setAttribute('id', 'topicSwitcher');
  select.addEventListener('change', e => {
    document.location = e.target.value;
  });
}

function renderLegend(ul) {
  if (ul) {
    Object.values(T.getLegend()).forEach(item => {
      const li = document.createElement('li');
      li.setAttribute('style', "color:"+item.color);
      li.appendChild(document.createTextNode(item.description));
      ul.appendChild(li);
    });
  }
}

function createPopup(feature, layer) {
  layer.bindPopup(T.getText(feature.properties))
}
