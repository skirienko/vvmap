import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import typeURL from './type.geojson?url';


type TypeGJProperties = {
  name: string,
  note?: string,
}

const TYPES: Record<string, LegendItem> = {
  's': {color:'#333333', description: 'улицы'},
  'l': {color:'#669966', description: 'переулки'},
  'p': {color:'#FF3333', description: 'проспекты'},
  'c': {color:'#663300', description: 'шоссе'},
  'e': {color:'#3366DD', description: 'набережные'},
  'b': {color:'#009933', description: 'бульвары'},
  'a': {color:'#33CC33', description: 'аллеи'},
  'm': {color:'#CC33CC', description: 'мосты'},
  'r': {color:'#FFDD66', description: 'кольца'},
  'd': {color:'#000099', description: 'проезды'},
  't': {color:'#990000', description: 'тупики'},
  'v': {color:'#666666', description: 'посёлки'},
}

export default class Gender extends Topic {
  topic = 'type';
  title = "Карта Владивостока — улицы по типам";
  legend = TYPES;
  getColor = this.getExactColor;
  getText = (p: TypeGJProperties) => p ? p.name : '';
  getURL = () => typeURL;
}