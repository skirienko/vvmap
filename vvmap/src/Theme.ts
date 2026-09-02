import { Topic, Legend } from "./Topic";
// @ts-ignore
import themeURL from './theme.geojson?url';
import { ExpressionSpecification } from "@maplibre/maplibre-gl-style-spec";
import { SCHEME } from "./colors";

type ThemeGJProps = {
    name: string,
    descr?: string,
}

const topic = 'theme';
// person, ship, tree, stone, place
const legend: Legend = {
    'person': {color: SCHEME.default, description: 'личность'},
    'ship': {color: SCHEME.blue, description: 'судно'},
    'place': {color: SCHEME.peach, description: 'место'},
    'tree': {color: SCHEME.green, description: 'дерево'},
    'flower': {color: SCHEME.purple, description: 'цветок'},
    'berry': {color: SCHEME.red, description: 'ягода'},
    'stone': {color:'black', description: 'камень'},
}

export default class Theme extends Topic {
    topic: string = topic;
    geojsonURL: string = themeURL;
    title: string = "Карта Владивостока — улицы по темам";
    legend: Legend = legend;
    maplibreColorMatch: ExpressionSpecification = this.mlColorMatch(topic);
    getText: (p: ThemeGJProps) => string = ({name, descr}: ThemeGJProps) => `<b>${name}</b><br>${descr}`;
}
