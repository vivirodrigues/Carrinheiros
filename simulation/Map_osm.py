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
    nodes = file.getElementsByTagName('junction')
    return list(nodes)


def get_edges(file):
    edge = file.getElementsByTagName('edge')
    return list(edge)


def create_node(osm_tag, id_node, lat, lon):
    version = '1'
    timestamp = '2021-02-15T04:31:59Z'
    changeset = '11916646'
    user = 'DS'
    uid = id_node
    new_node = {}
    new_node.update([('id', id_node), ('lat', lat),
                     ('lon', lon), ('version', version),
                     ('timestamp', timestamp), ('changeset', changeset),
                     ('uid', uid), ('user', user)])

    node = ET.Element("node")

    for i in list(new_node.keys()):
        node.attrib[i] = new_node.get(i)

    osm_tag.append(node)
    return osm_tag


def create_way(osm_tag, id_way, id_node_start, id_node_finish):
    version = '1'
    timestamp = '2021-02-15T04:31:59Z'
    changeset = '11916646'
    user = 'DS'
    uid = id_way

    new_way = {}
    new_way.update([('id', id_way), ('version', version),
                    ('timestamp', timestamp), ('changeset', changeset),
                    ('uid', uid), ('user', user)])

    nd_start = ET.Element("nd")
    nd_finish = ET.Element("nd")
    nd_start.attrib['ref'] = id_node_start
    nd_finish.attrib['ref'] = id_node_finish
    tag = ET.Element("tag")
    tag.attrib['k'] = 'highway'
    tag.attrib['v'] = 'residential'
    way = ET.Element("way")

    for i in list(new_way.keys()):
        way.attrib[i] = new_way.get(i)

    way.append(nd_start)
    way.append(nd_finish)
    way.append(tag)
    osm_tag.append(way)
    return osm_tag


def edges_net(name_net_xml):

    file = parse_file_minidom(name_net_xml)
    edges = get_edges(file)
    #  {'id_node_from', 'id_node_to'): 'id_edge'}
    edges_dict = {}
    for i in edges:
        if i.attributes['id'].value[0] != ':':
            edges_dict.update([((i.attributes['from'].value, i.attributes['to'].value), i.attributes['id'].value)])
    return edges_dict


if __name__ == '__main__':

    # print(nodes[0].attributes['lon'].value)

    file_2 = parse_file_tree('../data/maps/map.osm')
    osm_tag = file_2.getroot()

    dictionary = []
    for node in file_2.iter('way'):
        dictionary.append(node.items())
    #print(dictionary)



    #osm_tag = create_node(osm_tag, "2222", "2", "2")
    #osm_tag = create_way(osm_tag, "aaaa", "2222", "0000000000")

    #file_2.write("output.osm", xml_declaration=True)

    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    """
    # remove element
    for way in root.findall('country'):
        rank = int(way.find('rank').text)
        if rank > 50:
            root.remove(way)
    #file_2.write('output.xml')
    """
    #for node in file_2.iter('way'):
    #    print(node.attrib)

# https://dev.to/filipemot/criacao-de-xml-com-python-3fmd
# https://stackoverflow.com/questions/49924915/how-to-add-a-subchild-on-a-xml-file-using-xml-etree-elementtree/49925664
