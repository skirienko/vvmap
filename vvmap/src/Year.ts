import { Topic, LegendItem } from "./Topic";
// @ts-ignore
import yearURL from './year.geojson?url';

type YearGJProperties = {
  name: string,
  year: string,
}

const YEARS: Record<string, LegendItem> = {
  '1860': {from: '1860', to: '1907', color: '#1fc627', description: '1860—1907'},
  '1908': {from: '1908', to: '1921', color: '#0d7719', description: '1908—1921'},
  '1918': {from: '1918', to: '1922', color: '#ebcc04', description: '1918—1922'},
  '1923': {from: '1923', to: '1940', color: '#f90505', description: '1923—1940'},
  '1941': {from: '1941', to: '1952', color: '#d40b0b', description: '1941—1952'},
  '1953': {from: '1953', to: '1960', color: '#ba0b0b', description: '1953—1960'},
  '1961': {from: '1961', to: '1984', color: '#9c1111', description: '1961—1984'},
  '1985': {from: '1985', to: '1990', color: '#832f0e', description: '1985—1990'},
  '1991': {from: '1991', to: '2000', color: '#cc1eaf', description: '1991—2000'},
  '2001': {from: '2001', to: '2011', color: '#7627c0', description: '2001—2011'},
  '2012': {from: '2012', to: '2021', color: '#431ec6ff', description: '2012—2021'},
  '2022': {from: '2022', to: '2099', color: '#1212f3', description: '2022—н.в.'},
   '?': {from: '0', to: '0', color: '#99AA99', description: 'неизвестный год'},
}

export default class Year extends Topic {
  topic = 'year';
  title = "Карта Владивостока — улицы по годам";
  legend = YEARS;
  getColor = this.getRangeColor;
  getText = ({name, year}: YearGJProperties) => `${name}: ${year}`;
  getURL = () => yearURL;
}