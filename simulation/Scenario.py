import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET
from xml.dom import minidom
import random


def parse_file_minidom(name_file):
    return minidom.parse(name_file)


def parse_file_tree(name_file):
    tree = ET.parse(name_file)
    return tree


def get_nodes(file):
    nodes = file.getElementsByTagName('node')
    return list(nodes)


def get_ways(file):
    ways = file.getElementsByTagName('way')
    return list(ways)


def create_node(root_node, id_node, lat, lon):
    version = '1'
    timestamp = '2021-02-15T04:31:59Z'
    changeset = '11916646'
    user = 'DS'
    uid = id_node
    new_node = {}
    new_node.update([('id',id_node), ('lat', lat),
                     ('lon', lon), ('version', version),
                     ('timestamp',timestamp), ('changeset', changeset),
                     ('uid', uid), ('user', user)])

    for i in list(new_node.keys()):
        ET.SubElement(root_node, i).text = str(new_node.get(i))


if __name__ == '__main__':
    file = parse_file_minidom('../data/maps/map.osm')
    nodes = get_nodes(file)
    # print(nodes[0].attributes['lon'].value)
    n_nodes = len(nodes)

    file_2 = parse_file_tree('../data/maps/map.osm')
    root = file_2.getroot()
    #for child in root:
    #    print(child.tag)
    for node in root.iter('node'):
        print(node.attrib)

    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    for new in root.iter('node'):
        pass
    create_node(root, '11111', 0, 0)
    """
    # remove element
    for way in root.findall('country'):
        rank = int(way.find('rank').text)
        if rank > 50:
            root.remove(way)
    #file_2.write('output.xml')
    """
    for node in root.iter('node'):
        print(node.attrib)


