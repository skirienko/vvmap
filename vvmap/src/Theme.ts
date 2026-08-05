import {Topic, Legend, ColorGetter} from "./Topic";
// @ts-ignore
import themeURL from './theme.geojson?url';

type ThemeGJProps = {
    name: string,
    note?: string,
}

const topic = 'theme';
// person, ship, tree, stone, place
const THEMES: Legend = {
    'person': {color:'var(--street-default)', description: 'личность'},
    'ship': {color:'var(--street-blue)', description: 'судно'},
    'place': {color:'var(--street-yellow)', description: 'место'},
    'tree': {color:'var(--street-green)', description: 'дерево'},
    'flower': {color:'var(--street-purple)', description: 'цветок'},
    'berry': {color:'var(--street-red)', description: 'ягода'},
    'stone': {color:'black', description: 'камень'},
}

const ML_THEME = [
    'match',
    ['get', topic],
    'person', 'gray',
    'ship', 'blue',
    'place', 'brown',
    'tree', 'green',
    'flower', 'purple',
    'berry', 'red',
    'stone', 'black',
    'transparent'
];

export default class Theme extends Topic {
    topic: string = topic;
    title: string = "Карта Владивостока — улицы по темам";
    legend: Legend = THEMES;
    getColor: ColorGetter = this.getExactColor;
    maplibreColorMatch = ML_THEME;
    getText: (p: ThemeGJProps) => string = (p: ThemeGJProps) => p ? `${p.name}` : '';
    getURL = () => themeURL;
}
