import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
from Constants import *


def parse_file_minidom(name_file):
    return minidom.parse(name_file)


def parse_file_tree(name_file):
    tree = ET.parse(name_file)
    return tree


def get_nodes(file_name):
    # net file
    file = parse_file_minidom(file_name)
    nodes_list = file.getElementsByTagName('junction')
    nodes = [int(node.attributes['id'].value) for node in nodes_list if node.attributes['id'].value[0] != ':']
    return list(nodes)


def get_all_nodes(file):
    nodes = file.getElementsByTagName('junction')
    return list(nodes)


def get_edges(file):
    edge = file.getElementsByTagName('edge')
    return list(edge)


def node_coordinates(tree):
    dictionary_nodes = {}
    for node in tree.iter('node'):
        dictionary_nodes.update([(int(node.get('id')), (float(node.get('lat')), float(node.get('lon'))))])
    return dictionary_nodes


def create_node(osm_tag, id_node, lat, lon):
    version = '1'
    timestamp = '2021-02-15T04:31:59Z'
    changeset = '11916646'
    user = 'Carrinheiro'
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
    user = 'Carrinheiro'
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
    edges_dict = {}
    [edges_dict.update([((int(i.attributes['from'].value), int(i.attributes['to'].value)), str(i.attributes['id'].value))]) for i in edges if i.attributes['id'].value[0] != ':']

    return edges_dict


def nodes_z_net(name_net_xml):

    file = parse_file_minidom(name_net_xml)
    nodes = get_all_nodes(file)
    nodes_dict = {}
    [nodes_dict.update([(i.attributes['id'].value, float(i.attributes['z'].value))]) for i in nodes]#if i.attributes['id'].value[0] != ':']

    return nodes_dict


def edges_type(name_net_xml):
    file = parse_file_minidom(name_net_xml)
    edges = get_edges(file)
    #  {'id_node_from', 'id_node_to'): 'id_edge'}
    edges_dict = {}
    for i in edges:
        if i.attributes['id'].value[0] != ':':
            edges_dict.update(
                [((int(i.attributes['from'].value), int(i.attributes['to'].value)), str(i.attributes['type'].value).split(sep='.')[1:])])

    return edges_dict


def nodes_to_edges(nodes, edges_dict):
    """

    :param nodes:       list
                        list with id of nodes
    :return:            list
                        id of edges
    """
    edges_list = []
    for i in range(len(nodes)-1):

        edge = edges_dict.get((int(nodes[i]), int(nodes[i+1])))
        edges_list.append(edge)

    return edges_list


def edges_to_nodes(id_edge, edges_dict):
    """

    :param nodes:       list
                        list with id of nodes
    :return:            list
                        id of edges
    """

    nodes_list = list(edges_dict.keys())
    edges_id = list(edges_dict.values())

    id_edge = edges_id.index(id_edge)
    return nodes_list[id_edge]


def adjacent_nodes(edges_dict):

    nodes_pairs = list(edges_dict.keys())

    # dict with adjacent nodes of each node
    result = defaultdict(list)
    for key, val in nodes_pairs:
        result[key].append(val)

    return result


def delete_osm_items(osm_file, attrib='Carrinheiro'):
    tree = ET.parse(osm_file)
    for node in tree.iter():
        for child in node[:]:
            try:
                if child.attrib['user'] == attrib:
                    node.remove(child)
            except:
                pass

    tree.write(osm_file)


def edit_map(osm_file):

    root = minidom.parse(osm_file).documentElement

    # it transforms some edges in two ways streets
    x = root.getElementsByTagName("tag")
    new_x = []
    """
    for i in range(len(x)):
        if x[i].getAttribute("v") in TWO_WAY:
            new_x.append(x[i].parentNode.getAttribute("id"))
            print("oooo", x[i].parentNode.getAttribute("id"))
    """

    for i in range(len(x)):
        if x[i].getAttribute("k") == 'oneway' or x[i].getAttribute("v") == 'roundabout' or x[i].getAttribute("k") == 'restriction' or x[i].getAttribute("v") == 'restriction':
        #if x[i].getAttribute("v") == 'roundabout' or x[i].getAttribute("k") == 'restriction' or x[i].getAttribute("v") == 'restriction':
            x[i].parentNode.removeChild(x[i])

    # it transforms some edges types in "residential"
    x = root.getElementsByTagName("tag")

    possibilities = ['cycleway', 'service', 'sidewalk', 'footway', 'crossing', 'pedestrian']
    for i in range(len(x)):
        if x[i].getAttribute("v") in possibilities:
            x[i].attributes["v"].value = "residential"

    with open(osm_file, "w") as fs:
        fs.write(root.toxml())
        fs.close()


def allow_vehicle(net_file):

    root = minidom.parse(net_file).documentElement

    # allow the vehicle
    x = root.getElementsByTagName("lane")

    for i in range(len(x)):
        text = x[i].getAttribute("allow")
        if len(text) > 0:
            x[i].attributes["allow"].value = text + " " + VEHICLE

    with open(net_file, "w") as fs:
        fs.write(root.toxml())
        fs.close()


if __name__ == '__main__':

    # print(nodes[0].attributes['lon'].value)

    #file_2 = parse_file_tree('../data/maps/map.osm')
    # osm_tag = file_2.getroot()

    a = '../data/maps/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925.osm'
    delete_osm_items(a)

    #dictionary = {}
    #for node in file_2.iter('node'):
    #    dictionary.update([(float(node.get('id')), (float(node.get('lat')), float(node.get('lon'))))])
    #print(dictionary)




    #osm_tag = create_node(osm_tag, "2222", "2", "2")
    #osm_tag = create_way(osm_tag, "aaaa", "2222", "0000000000")

    #file_2.write("output.osm", xml_declaration=True)

    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')



    #y = x.childNodes #.getAttribute("id")

    #x.removeChild(y)
    #file_2.write('output.xml')

    #for node in file_2.iter('node'):
    #    print(node.attrib)

# https://dev.to/filipemot/criacao-de-xml-com-python-3fmd
# https://stackoverflow.com/questions/49924915/how-to-add-a-subchild-on-a-xml-file-using-xml-etree-elementtree/49925664
