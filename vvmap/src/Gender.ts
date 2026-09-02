import { Topic, Legend } from "./Topic";
// @ts-ignore
import genderURL from './gender.geojson?url';
import { ExpressionSpecification } from "@maplibre/maplibre-gl-style-spec";
import { SCHEME } from './colors';


type GenderGJProperties = {
  name: string,
  part: string,
}

const topic = 'gender';

const legend: Legend = {
  'f': {color: SCHEME.red, description: 'в честь женщин'},
  'm': {color: SCHEME.blue, description: 'в честь мужчин'},
  '-': {color: SCHEME.neutral, description: 'нейтральные'},
  '!': {color: SCHEME.purple, description: 'как бы нейтральные, но вообще-то в честь мужчин'},
  '?': {color: SCHEME.yellow, description: 'непонятно'},
}

export default class Gender extends Topic {
  topic: string = topic;
  geojsonURL: string = genderURL;
  title: string = "Карта Владивостока — улицы по гендерному признаку";
  legend: Legend = legend;
  maplibreColorMatch: ExpressionSpecification = this.mlColorMatch(topic);
  getText: (p: GenderGJProperties) => string = (p: GenderGJProperties) => p ? `<b>${p.name}</b><br>${p.part}` : '';
}
