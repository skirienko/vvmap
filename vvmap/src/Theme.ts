import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import typeURL from './theme.geojson?url';


type ThemeGJProperties = {
    name: string,
    note?: string,
}
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

export default class Theme extends Topic {
    topic = 'theme';
    title = "Карта Владивостока — улицы по темам";
    legend = THEMES;
    getColor = this.getExactColor;
    getText = (p: ThemeGJProperties) => p ? `${p.name}` : '';
    getURL = () => typeURL;
}
