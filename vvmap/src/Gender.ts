import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import genderURL from './gender.geojson?url';


type GenderGJProperties = {
  name: string,
}

const GENDERS: Record<string, LegendItem> = {
  'f': {color:'var(--street-red)', description: 'в честь женщин'},
  'm': {color:'var(--street-blue)', description: 'в честь мужчин'},
  '-': {color:'var(--street-neutral)', description: 'нейтральные'},
  '!': {color:'var(--street-purple)', description: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color:'var(--street-yellow)', description: 'непонятно'},
}

export default class Gender extends Topic {
  topic = 'gender';
  title = "Карта Владивостока — улицы по гендерному признаку";
  legend = GENDERS;
  getColor = this.getExactColor;
  getText = (p: GenderGJProperties) => p ? p.name : '';
  getURL = () => genderURL;
}