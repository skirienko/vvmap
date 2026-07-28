import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import typeURL from './theme.geojson?url';

type ThemeGJProperties = {
    name: string,
    note?: string,
}

const topic = 'theme';
// person, ship, tree, stone, place
const THEMES: Record<string, LegendItem> = {
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
    'place', 'yellow',
    'tree', 'green',
    'flower', 'purple',
    'berry', 'red',
    'stone', 'black',
    'transparent'
];

export default class Theme extends Topic {
    topic = topic;
    title = "Карта Владивостока — улицы по темам";
    legend = THEMES;
    getColor = this.getExactColor;
    maplibreColorMatch = ML_THEME;
    getText = (p: ThemeGJProperties) => p ? `${p.name}` : '';
    getURL = () => typeURL;
}
