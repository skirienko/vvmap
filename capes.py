import json

path = 'justcapes.osm'
capes = []

# default: left
ANCHORS = {
    'мыс Артур': 'bottom-right',
    'мыс Абросимова': 'right',
    'мыс Безымянный': 'bottom-right',
    'мыс Боброва': 'bottom-right',
    'мыс Бурный': 'bottom-right',
    'мыс Вязкий': 'bottom-right',
    'мыс Голдобина': 'top-right',
    'мыс Грозный': 'top-right',
    'мыс Дальний': 'bottom-left',
    'мыс Калузина': 'right',
    'мыс Клета': 'right',
    'мыс Клыкова': 'right',
    'мыс Красный': 'bottom-right',
    'мыс Кузнецова': 'right',
    'мыс Купера': 'bottom-right',
    'мыс Лагерный': 'bottom-right',
    'мыс Марковского': 'bottom-right',
    'мыс Назимова': 'top-right',
    'мыс Острый': 'top-right',
    'мыс Россета': 'bottom-right',
    'мыс Соловьёва': 'top-right',
    'мыс Спорный': 'bottom-right',
    'мыс Токаревского': 'right',
    'мыс Тупой': 'bottom-right',
    'мыс Фирсова': 'bottom-right',
    'мыс Чуркина': 'right',
    'мыс Щетининой': 'right',
}


def parse_json():
    with(open(path, 'r')) as f:
        res = json.load(f)

    if res and 'elements' in res:
        for el in res['elements']:
            if el['type'] == 'node' and 'tags' in el:
                capes.append(el)
            elif el['type'] != 'node':
                print(el)
        print(capes)

        generate_geojson(capes)

def get_anchor(cape):
    if cape['tags']['name'] in ANCHORS:
        return ANCHORS[cape['tags']['name']]

    return 'left'


def generate_geojson(store):
    geojson = {'type': 'FeatureCollection', 'features': []}

    for cape in store:
        feat = {'type': 'Feature', 'geometry': {"type": "Point", 'coordinates': []}, 'properties': {}}
        for tag in cape['tags']:
            feat['properties'][tag] = cape['tags'][tag]
        feat['properties']['anchor'] = get_anchor(cape)
        feat['geometry']['coordinates'] = [cape['lon'], cape['lat']]
        geojson['features'].append(feat)


    with open(f'./vvmap/src/capes.geojson', 'w') as fd:
        fd.write(json.dumps(geojson, ensure_ascii=False))



def main():
    print('Parsing geodata...')
    parse_json()

if __name__ == '__main__':
    main()
