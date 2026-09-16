import json

path = 'justcapes.osm'
capes = []

ANCHORS = {
    'мыс Абросимова': 'right',
    'мыс Голдобина': 'top-right',
    'мыс Клета': 'right',
    'мыс Купера': 'bottom-right',
    'мыс Острый': 'top-right',
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
