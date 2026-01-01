export type LegendItem = {
  color: string;
  description: string;
  from?: string;
  to?: string;
}


export abstract class Topic {

  title: string = "Карта Владивостока";
    
  legend: Record<string, LegendItem> = {};

  getTitle() {
    return this.title;
  }
  
  getLegend() {
    return this.legend;
  }

  getExactColor(key: string) {
    return key in this.legend ? this.legend[key].color : this.legend['?'].color;
  }

  getRangeColor(value: string) {
    const isInRange = (i:LegendItem) =>  i.from && i.to && value >= i.from && value <= i.to;
    const item = Object.values(this.legend).find(isInRange) ?? this.legend['?'];
    return item.color;
  }
}