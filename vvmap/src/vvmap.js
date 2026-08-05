import mapstyleURL from './posi.json';
import mapstyleDarkURL from './posi-dark.json';

import {Map, Popup, setWorkerUrl} from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';

setWorkerUrl(workerUrl);

import Router from './Router';

import Gender from './Gender';
import Year from './Year';
import Type from './Type';
import Theme from "./Theme.ts";

import 'maplibre-gl/dist/maplibre-gl.css';

let T;
let legend;

const sources = {};
const layerId = 'color-layer';

const map = new Map({
  container: 'map',
  style: mapstyleURL,
  center: [131.905, 43.103],
  zoom: 12
});

const routes = [
  { path: '/gender', description: 'улицы по полу', callback: initMap.bind(this, Gender) },
  { path: '/year', description: 'улицы по годам', callback: initMap.bind(this, Year) },
  { path: '/type', description: 'улицы по типам', callback: initMap.bind(this, Type) },
  { path: '/theme', description: 'улицы по темам', callback: initMap.bind(this, Theme) },
];
let router;

map.once('load', () => {
  // The router invokes the initial callback synchronously. Start it only
  // after MapLibre can safely add sources and layers.
  router = new Router(routes);
  renderSwitcher(switcher);
});

function initMap(type) {
  T = new type();
  document.title = T.getTitle();
  renderLegend(legend);
  loadLayer(T);
}

map.on('click', layerId, (e) => {
  new Popup().setLngLat(e.lngLat)
      .setHTML(T.getText(e.features[0].properties))
      .addTo(map);
});

map.on('mouseenter', layerId, (e) => {
  map.getCanvas().style.cursor = 'pointer';
});

map.on('mouseleave', layerId, (e) => {
  map.getCanvas().style.cursor = '';
});

function loadLayer(T) {
  const srcId = `src-${T.topic}`;

  if (!sources[srcId]) {
    sources[srcId] = map.addSource(srcId, {
      type: 'geojson',
      data: T.getURL(),
    });
  }

  if (map.getLayer(layerId)) {
    map.removeLayer(layerId);
  }
  map.addLayer({
    id: layerId,
    source: srcId,
    type: 'line',
    layout: {
      'line-join': 'round',
      'line-cap': 'round'
    },
    paint: {
      'line-width': [
        "interpolate",
        ["exponential", 1.5],
        ["zoom"],
        15,
        3,
        17,
        10
      ],
      'line-layer-opacity': .5,
      'line-color': T.maplibreColorMatch,
    }
  }, 'highway-name-path');
}

const switcher = document.querySelector('.switcher');
legend = document.querySelector('.legend');

function renderSwitcher(select) {
  routes.forEach(r => {
    const option = document.createElement('option');
    option.setAttribute('value', r.path);
    if (r === router.getCurrentRoute()) {
      option.setAttribute('selected', 'true');
    }
    option.appendChild(document.createTextNode(r.description));
    select.appendChild(option);
  });
  select.setAttribute('id', 'topicSwitcher');
  select.addEventListener('change', e => {
    router.navigateTo(e.target.value);
  });
}

function renderLegend(ul) {
  if (ul && T) {
    legend.replaceChildren();
    Object.values(T.getLegend()).forEach(item => {
      const li = document.createElement('li');
      li.setAttribute('style', "color:"+item.color);
      li.appendChild(document.createTextNode(item.description));
      ul.appendChild(li);
    });
  }
}
