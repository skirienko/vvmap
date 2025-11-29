import * as L from 'leaflet';
import '@maplibre/maplibre-gl-leaflet';
import mapstyleURL from './posi.json';
import streetsURL from './gender.geojson?url';

import 'leaflet/dist/leaflet.css';
import 'maplibre-gl/dist/maplibre-gl.css';

const GENDERS = {
  'f': {color:'#FF3333', description: 'улицы в честь женщин'},
  'm': {color:'#3333FF', description: 'улицы в честь мужчин'},
  '-': {color:'#99AA99', description: 'нейтральные улицы'},
  '!': {color:'#CC33CC', description: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color:'#FFDD66', description: 'непонятно'},
}

const YEARS = {
  '?': {color: '#99AA99', description: 'неизвестный год'},
  '1955': {color: '#AA2222', description: '1955'},
  '2016': {color: '#2222AA', description: '2016'},
  '2020': {color: '#2222DB', description: '2020'},
  '2021': {color: '#2222DD', description: '2021'},
  '2022': {color: '#2222DF', description: '2022'},
  '2023': {color: '#2222EA', description: '2023'},
  '2024': {color: '#2222EC', description: '2024'},
  '2025': {color: '#2222EE', description: '2025'},
}

//const topic = 'gender';
const topic = 'gender';
const LEGEND = GENDERS;

const map = L.map('map', {attributionControl:false}).setView([43.103, 131.905], 12);

const gl = L.maplibreGL({
          // style: 'https://tiles.openfreemap.org/styles/positron'
          style: mapstyleURL,
          maxZoom: 19
        }).addTo(map);

const st = ({properties}) => {
  return {opacity:.75, color:getColor(properties[topic])}
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
  console.log(key);
  return key in LEGEND ? LEGEND[key].color : LEGEND['?'].color
}
