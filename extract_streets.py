import xml.etree.ElementTree as ET
import json
from simplification.cutil import (
    simplify_coords,
    simplify_coords_vw,
)

filepath = 'map.osm'

nodes = {}
streets = {}
ways = {}
genders = {}

def parseXML():
    tree = ET.parse(filepath)
    root = tree.getroot()

    print('Collecting nodes...')
    for nd in root.findall('./node'):
        nodes[nd.attrib['id']] = (float(nd.attrib['lat']), float(nd.attrib['lon']))
    
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
        if (w.find('./tag[@k="highway"]') is not None):
            n = w.find('./tag[@k="name"]')
            if (n is not None):
                name = n.attrib['v']
                if name not in ways:
                    print(name)
                    ways[name] = {'parts':[]}
                nd = w.findall('./nd')
                if len(nd):
                    el = get_nodes(nd)
                    ways[name]['parts'].append(el)
    
    print(f'{len(ways)} ways collected')
 
    load_genders()

    result = {}
    unknown = []
    for name in ways:
        if name in genders:
            result[name] = ways[name]
            result[name]['gender'] = genders[name]
        else:
            unknown.append(name)

    with open('./vvmap/streets.json', 'w') as fd:
        fd.write(json.dumps(result, ensure_ascii=False))

    with open('unknown_streets.txt', 'w') as ud:
        for name in unknown:
            ud.write(f'{name}\r\n')


def get_nodes(nd):
    refs = [n.attrib['ref'] for n in nd]
    # line simplification
    unsimplified = [nodes[r] for r in refs]
    # simplify_coords_vw supposed to be slower but nicer
    simplified = simplify_coords(unsimplified, 0.0001)
    return simplified


def load_genders():
    lines = []
    with open('streets_genders.csv', 'r') as fd:
        lines = fd.readlines()

    for line in lines:
        line = line.strip()
        row = line.split(',')
        if (len(row) > 1):
            genders[row[0]] = row[1]


def main():
    print('Parsing...')
    parseXML()

if __name__ == '__main__':
    main()