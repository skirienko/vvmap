import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import genderURL from './gender.geojson?url';


type GenderGJProperties = {
  name: string,
  part: string,
}

const topic = 'gender';

const GENDERS: Record<string, LegendItem> = {
  'f': {color:'var(--street-red)', description: 'в честь женщин'},
  'm': {color:'var(--street-blue)', description: 'в честь мужчин'},
  '-': {color:'var(--street-neutral)', description: 'нейтральные'},
  '!': {color:'var(--street-purple)', description: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color:'var(--street-yellow)', description: 'непонятно'},
}

const ML_GENDER = [
  'match',
  ['get', topic],
  'f', 'red',
  'm', 'blue',
  '-', 'gray',
  '!', 'purple',
  '?', 'yellow',
  'transparent'
];

export default class Gender extends Topic {
  topic = topic;
  title = "Карта Владивостока — улицы по гендерному признаку";
  legend = GENDERS;
  getColor = this.getExactColor;
  maplibreColorMatch = ML_GENDER;
  getText = (p: GenderGJProperties) => p ? `<b>${p.name}</b><br>${p.part}` : '';
  getURL = () => genderURL;
}
