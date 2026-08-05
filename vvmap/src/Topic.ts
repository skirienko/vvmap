export type LegendItem = {
  color: string;
  description: string;
  from?: string;
  to?: string;
}

export type Legend = Record<string, LegendItem>;

export type ColorGetter = (key: string) => string;

export abstract class Topic {

  title: string = "Карта Владивостока";
    
  legend: Legend = {};

  maplibreColorMatch?: any[];

  getTitle(): string {
    return this.title;
  }
  
  getLegend(): Legend {
    return this.legend;
  }

  getExactColor(key: string): string {
    return key in this.legend ? this.legend[key].color : this.legend['?'].color;
  }

  getRangeColor(value: string): string {
    const isInRange = (i:LegendItem) =>  i.from && i.to && value >= i.from && value <= i.to;
    const item = Object.values(this.legend).find(isInRange) ?? this.legend['?'];
    return item.color;
  }

}