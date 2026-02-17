import xml.etree.ElementTree as ET
import json
from simplification.cutil import (
    simplify_coords,
    simplify_coords_vw,
)

filepath = 'vladivostok.osm'

nodes = {}
nodes2 = {}
streets = {}
ways = {}
ways2 = {}

def parse_xml():
    tree = ET.parse(filepath)
    root = tree.getroot()

    print('Collecting nodes...')
    for nd in root.findall('./node'):
        nodes[nd.attrib['id']] = (float(nd.attrib['lat']), float(nd.attrib['lon']))
        nodes2[nd.attrib['id']] = (float(nd.attrib['lon']), float(nd.attrib['lat']))
    
    # print(f'{len(nodes)} nodes collected')

    #for tag in root.findall('./way/tag[@k="addr:street"]'):
    #    streets[tag.attrib['v']] = ()

    #for st in streets:
    #    print(st)

    #print(f'{len(streets)} streets collected')

    #with open('streets.csv', 'w') as fd:
    #    for st in streets:
    #        fd.write(f'{st},-\r\n')

    print('Collecting ways...')
    
    # for w in root.findall('./way/tag[@k="highway"]/..'):
    for w in root.findall('./way[tag]'):
        if w.find('./tag[@k="highway"]') is not None:
            n = w.find('./tag[@k="name"]')
            if n is not None:
                name = n.attrib['v']
                if name not in ways:
                    print(name)
                    ways[name] = {'parts':[]}
                    ways2[name] = []
                nd = w.findall('./nd')
                if len(nd):
                    ways[name]['parts'].append(get_nodes(nd))
                    ways2[name].append(get_nodes2(nd))
    
    print(f'{len(ways)} ways collected')
 
    generate_geojson('gender', load_genders())
    generate_geojson('year', load_years())
    generate_geojson('type', load_types())


def generate_geojson(topic, store):
    result = {}
    geojson = {}
    unknown = []
    unused = []

    for name in ways:
        if name.lower() in store:
            src = store[name.lower()]
            result[name] = ways[name]
            result[name][topic] = src['value']
            if 'descr' in src:
                result[name]['descr'] = src['descr']
            src['used'] += 1
        else:
            unknown.append(name)

    geojson['type'] = 'FeatureCollection'
    geojson['features'] = []
    for name in result:
        feat = {'type': 'Feature', 'properties': {}}
        feat['properties']['name'] = name
        feat['properties'][topic] = result[name][topic]
        if 'descr' in result[name]:
            feat['properties']['descr'] = result[name]['descr']
        feat['geometry'] = {}
        if len(ways2[name]) == 1:
            feat['geometry']['type'] = 'LineString'
            feat['geometry']['coordinates'] = ways2[name][0]
        else:
            feat['geometry']['type'] = 'MultiLineString'
            feat['geometry']['coordinates'] = ways2[name]
        geojson['features'].append(feat)

    with open(f'./vvmap/src/{topic}.geojson', 'w') as fd:
        fd.write(json.dumps(geojson, ensure_ascii=False))

    with open(f'unknown_streets_{topic}.txt', 'w') as ud:
        for name in unknown:
            ud.write(f'{name}\r\n')

    with open(f'unused_streets_{topic}.txt', 'w') as uud:
        for key in store.keys():
            if store[key]['used'] == 0:
                i = store[key]
                uud.write(f'{i["name"]}: {i["used"]}\r\n')


def get_nodes(nd):
    refs = [n.attrib['ref'] for n in nd]
    # line simplification
    unsimplified = [nodes[r] for r in refs]
    # simplify_coords_vw supposed to be slower but nicer
    #simplified = simplify_coords(unsimplified, 0.0001)
    return unsimplified


def get_nodes2(nd):
    refs = [n.attrib['ref'] for n in nd]
    # line simplification
    unsimplified = [nodes2[r] for r in refs]
    # simplify_coords_vw supposed to be slower but nicer
    # simplified = simplify_coords_vw(unsimplified, 0.0001)
    return unsimplified


def read_lines(filename):
    lines = []
    with open(filename, 'r') as fd:
        lines = fd.readlines()
    
    return lines


def load_genders():
    lines = read_lines('streets_genders.csv')
    result = {}
    for line in lines:
        line = line.strip()
        row = line.split(',')
        key = row[0].lower()
        if len(row) > 1:
            result[key] = {'name': row[0], 'value': row[1], 'used': 0}
    return result


def load_years():
    lines = read_lines('streets_years.csv')
    result = {}
    for line in lines:
        line = line.strip()
        row = line.split(';')
        key = row[0].lower()
        if len(row) > 1:
            if row[1] != '-':
                feature = {'name': row[0], 'value': row[1], 'used': 0}
                if len(row) > 2:
                    feature['descr'] = row[2]
                result[key] = feature
    return result


def load_types():
    lines = read_lines('streets_types.csv')
    result = {}
    for line in lines:
        line = line.strip()
        row = line.split(',')
        key = row[0].lower()
        if len(row) > 1:
            if row[1] != '-':
                result[key] = {'name': row[0], 'value': row[1], 'used': 0}
    return result

def main():
    print('Parsing...')
    parse_xml()

if __name__ == '__main__':
    main()