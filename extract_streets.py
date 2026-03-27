import re
import xml.etree.ElementTree as ET
import json
from simplification.cutil import (
    simplify_coords,
    simplify_coords_vw,
)

filepath = 'vladivostok.osm'

PART_RELATIONS = {
    '7063164': 'russky',
    '2247428': 'popova',
    '1933752': 'reineke',
    '7310557': 'peschany',
    '3372537': 'trudovoe',
}

PART_NAMES = {
    'russky': 'Русский',
    'popova': 'Попова',
    'reineke': 'Рейнеке',
    'peschany': 'Песчаный',
    'trudovoe': 'Трудовое',
}

nodes = {}
nodes2 = {}
streets = {}
ways = {}
ways2 = {}
osm_ways = {}
part_polygons = {}

def parse_xml():
    tree = ET.parse(filepath)
    root = tree.getroot()

    print('Collecting nodes...')
    for nd in root.findall('./node'):
        nodes[nd.attrib['id']] = (float(nd.attrib['lat']), float(nd.attrib['lon']))
        nodes2[nd.attrib['id']] = (float(nd.attrib['lon']), float(nd.attrib['lat']))
    
    print('Collecting relation geometries...')
    collect_osm_ways(root)
    collect_part_polygons(root)

    print('Collecting ways...')

    for w in root.findall('./way[tag]'):
        if is_named_street(w):
            name = w.find('./tag[@k="name"]').attrib['v']
            nd = w.findall('./nd')
            if len(nd):
                part = classify_way(nd)
                key = make_way_key(name, part)
                if key not in ways:
                    print(f'{name} [{part}]')
                    ways[key] = {'name': name, 'part': part, 'parts': []}
                    ways2[key] = []
                ways[key]['parts'].append(get_nodes(nd))
                ways2[key].append(get_nodes2(nd))
    
    print(f'{len(ways)} ways collected')
 
    generate_geojson('gender', load_genders())
    generate_geojson('year', load_years())
    generate_geojson('type', load_types())


def generate_geojson(topic, store):
    result = {}
    geojson = {}
    unknown = []

    for key in ways:
        way = ways[key]
        name = way['name']
        key2 = name.lower()
        src = None
        if way['part'] != 'mainland':
            key3 = key2 + ' (' + PART_NAMES[way['part']].lower() +')'
            if key3 in store:
                src = store[key3]
            elif key2 in store:
                src = store[key2]
        elif key2 in store:
            src = store[key2]

        if src:
            result[key] = way
            result[key][topic] = src['value']
            if 'descr' in src:
                result[key]['descr'] = src['descr']
            src['used'] += 1
        else:
            unknown.append(f'{name} [{way["part"]}]')

    geojson['type'] = 'FeatureCollection'
    geojson['features'] = []
    for key in result:
        name = result[key]['name']
        feat = {'type': 'Feature', 'properties': {}}
        feat['properties']['name'] = name
        feat['properties']['part'] = result[key]['part']
        feat['properties'][topic] = result[key][topic]
        if 'descr' in result[key]:
            feat['properties']['descr'] = result[key]['descr']
        feat['geometry'] = {}
        if len(ways2[key]) == 1:
            feat['geometry']['type'] = 'LineString'
            feat['geometry']['coordinates'] = ways2[key][0]
        else:
            feat['geometry']['type'] = 'MultiLineString'
            feat['geometry']['coordinates'] = ways2[key]
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


def is_named_street(way):
    has_name = way.find('./tag[@k="name"]') is not None
    if not has_name:
        return False
    return (
        way.find('./tag[@k="highway"]') is not None
        or way.find('./tag[@k="bridge"][@v="yes"]') is not None
    )


def make_way_key(name, part):
    return f'{name}::{part}'


def classify_way(nd):
    coords = get_nodes2(nd)
    hits = {}
    for point in coords:
        for part, polygons in part_polygons.items():
            if contains_point(polygons, point):
                hits[part] = hits.get(part, 0) + 1
    if hits:
        return max(hits, key=hits.get)

    point = representative_point(coords)
    for part, polygons in part_polygons.items():
        if contains_point(polygons, point):
            return part
    return 'mainland'


def representative_point(coords):
    lon = sum(point[0] for point in coords) / len(coords)
    lat = sum(point[1] for point in coords) / len(coords)
    return lon, lat


def contains_point(polygons, point):
    for polygon in polygons:
        if not polygon:
            continue
        if point_in_ring(point, polygon[0]) and not any(
            point_in_ring(point, hole) for hole in polygon[1:]
        ):
            return True
    return False


def point_in_ring(point, ring):
    x, y = point
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def collect_osm_ways(root):
    for way in root.findall('./way'):
        refs = [nd.attrib['ref'] for nd in way.findall('./nd')]
        if refs:
            osm_ways[way.attrib['id']] = refs


def collect_part_polygons(root):
    for rel in root.findall('./relation'):
        rel_id = rel.attrib['id']
        if rel_id not in PART_RELATIONS:
            continue
        part = PART_RELATIONS[rel_id]
        polygons = build_relation_polygons(rel)
        if polygons:
            part_polygons[part] = polygons
    print(f'{len(part_polygons)} part polygons collected')


def build_relation_polygons(rel):
    outers = []
    inners = []
    for member in rel.findall('./member'):
        if member.attrib.get('type') != 'way':
            continue
        refs = osm_ways.get(member.attrib['ref'])
        if not refs:
            continue
        ring = refs_to_ring(refs)
        if not ring:
            continue
        coords = [nodes2[r] for r in ring if r in nodes2]
        if len(coords) < 4:
            continue
        if member.attrib.get('role') == 'inner':
            inners.append(coords)
        else:
            outers.append(coords)

    polygons = [[outer] for outer in outers]
    for inner in inners:
        attached = False
        for polygon in polygons:
            if point_in_ring(inner[0], polygon[0]):
                polygon.append(inner)
                attached = True
                break
        if not attached:
            polygons.append([inner])
    return polygons


def refs_to_ring(refs):
    ring = refs[:]
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    return ring


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
                rx_name = re.compile(r'(.*) \((.*)\)$')
                name = row[0]
                part = ''
                mo = rx_name.match(name)
                if mo:
                    name = mo.group(1)
                    part = mo.group(2)
                feature = {'name': name, 'part': part, 'value': row[1], 'used': 0}
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
