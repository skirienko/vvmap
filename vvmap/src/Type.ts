import {Topic, Legend} from "./Topic";
// @ts-ignore
import typeURL from './type.geojson?url';
import {
  ExpressionSpecification
} from "@maplibre/maplibre-gl-style-spec";
import {SCHEME} from "./colors";

type TypeGJProps = {
  name: string,
  note?: string,
  part: string,
}

const topic = 'type';

const legend: Legend = {
  's': {color: SCHEME.default, description: 'улицы'},
  'l': {color: SCHEME.neutral, description: 'переулки'},
  'p': {color: SCHEME.red, description: 'проспекты'},
  'c': {color:'#663300', description: 'шоссе'},
  'e': {color: SCHEME.blue, description: 'набережные'},
  'b': {color:'#009933', description: 'бульвары'},
  'a': {color:'#33CC33', description: 'аллеи'},
  'm': {color: SCHEME.purple, description: 'мосты'},
  'r': {color: SCHEME.yellow, description: 'кольца'},
  'd': {color:'#000099', description: 'проезды'},
  't': {color:'#990000', description: 'тупики'},
  'v': {color:'#339999', description: 'посёлки'},
}

export default class Gender extends Topic {
  topic: string = topic;
  geojsonURL: string = typeURL;
  title: string = "Карта Владивостока — улицы по типам";
  legend: Legend = legend;
  maplibreColorMatch: ExpressionSpecification = this.mlColorMatch(topic);
  getText: (p: TypeGJProps) => string = (p: TypeGJProps) => p ? `<b>${p.name}</b><br>${p.part}` : '';
}
