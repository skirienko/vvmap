import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import typeURL from './type.geojson?url';


type TypeGJProperties = {
  name: string,
  note?: string,
}

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

export default class Gender extends Topic {
  topic = 'type';
  title = "Карта Владивостока — улицы по типам";
  legend = TYPES;
  getColor = this.getExactColor;
  getText = (p: TypeGJProperties) => p ? p.name : '';
  getURL = () => typeURL;
}