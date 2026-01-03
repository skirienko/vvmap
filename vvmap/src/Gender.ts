import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import genderURL from './gender.geojson?url';


type GenderGJProperties = {
  name: string,
}

const GENDERS: Record<string, LegendItem> = {
  'f': {color:'#FF3333', description: 'улицы в честь женщин'},
  'm': {color:'#3333FF', description: 'улицы в честь мужчин'},
  '-': {color:'#99AA99', description: 'нейтральные улицы'},
  '!': {color:'#CC33CC', description: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color:'#FFDD66', description: 'непонятно'},
}

export default class Gender extends Topic {
  topic = 'gender';
  title = "Карта Владивостока — улицы по гендерному признаку";
  legend = GENDERS;
  getColor = this.getExactColor;
  getText = (p: GenderGJProperties) => p ? p.name : '';
  getURL = () => genderURL;
}