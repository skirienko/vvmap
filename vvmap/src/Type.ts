import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import typeURL from './type.geojson?url';

type TypeGJProperties = {
  name: string,
  note?: string,
  part: string,
}

const topic = 'type';

const TYPES: Record<string, LegendItem> = {
  's': {color:'var(--street-default)', description: 'улицы'},
  'l': {color:'var(--street-neutral)', description: 'переулки'},
  'p': {color:'var(--street-red)', description: 'проспекты'},
  'c': {color:'#663300', description: 'шоссе'},
  'e': {color:'var(--street-blue)', description: 'набережные'},
  'b': {color:'#009933', description: 'бульвары'},
  'a': {color:'#33CC33', description: 'аллеи'},
  'm': {color:'var(--street-purple)', description: 'мосты'},
  'r': {color:'var(--street-yellow)', description: 'кольца'},
  'd': {color:'#000099', description: 'проезды'},
  't': {color:'#990000', description: 'тупики'},
  'v': {color:'#339999', description: 'посёлки'},
}

const ML_TYPE = [
  'match',
  ['get', topic],
  's', '#808080',
  'l', '#9aab9a',
  'p', 'red',
  'c', '#663300',
  'e', 'blue',
  'b', '#009933',
  'a', '#33CC33',
  'm', 'purple',
  'r', 'yellow',
  'd', '#000099',
  't', '#990000',
  'v', '#339999',
  'transparent'
];

export default class Gender extends Topic {
  topic = topic;
  title = "Карта Владивостока — улицы по типам";
  legend = TYPES;
  getColor = this.getExactColor;
  maplibreColorMatch = ML_TYPE;
  getText = (p: TypeGJProperties) => p ? `<b>${p.name}</b><br>${p.part}` : '';
  getURL = () => typeURL;
}
