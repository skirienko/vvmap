import {Topic, Legend, ColorGetter} from "./Topic";
// @ts-ignore
import genderURL from './gender.geojson?url';


type GenderGJProperties = {
  name: string,
  part: string,
}

const topic = 'gender';

const GENDERS: Legend = {
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
  topic: string = topic;
  title: string = "Карта Владивостока — улицы по гендерному признаку";
  legend: Legend = GENDERS;
  getColor: ColorGetter = this.getExactColor;
  maplibreColorMatch = ML_GENDER;
  getText = (p: GenderGJProperties) => p ? `<b>${p.name}</b><br>${p.part}` : '';
  getURL = () => genderURL;
}
