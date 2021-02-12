import osmnx as ox
import numpy as np
import sys
import pandas as pd
import networkx as nx
import rasterio
# matplotlib inline
ox.config(log_console=True)
ox.__version__

# settings.py -> mudar "google" para o método geotiff

def getCoordinatePixel(map,lon,lat):
    # open map
    dataset = rasterio.open(map)
    # get pixel x+y of the coordinate
    py, px = dataset.index(lon, lat)
    # create 1x1px window of the pixel
    window = rasterio.windows.Window(px - 1//2, py - 1//2, 1, 1)
    # read rgb values of the window
    clip = dataset.read(window=window)
    #print(clip)
    return(clip[0][0][0]) #,clip[1][0][0],clip[2][0][0])

# lat-lon -22.796008, -22.843953, -47.054891, -47.107718000000006
G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
#G = ox.graph_from_bbox(-22.826008, -22.843953, -47.094891, -47.107718000000006, network_type='all')
# G = ox.add_node_elevations(G, api_key="AIzaSyC8PuUDUsWTMAmQGETWRLUCSHXwiMdgj30")
# G = ox.add_edge_grades(G)
# G_projected = ox.project_graph(G)
#ox.io.save_graphml(G, filepath='../map1.graphml')
# ox.plot_graph(G_projected)
# nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma')
# fig, ax = ox.plot_graph(G, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')
node_points = pd.Series(
    {node: f'{data["y"]:.5f},{data["x"]:.5f}' for node, data in G.nodes(data=True)}
)
# print(node_points)
x = nx.get_node_attributes(G, "x")
x1 = list(x.values())
y = nx.get_node_attributes(G, "y")
y1 = list(y.values())
keys = list(y.keys())
elevation = []
for i in range(0, len(x)):
    elevation.append(getCoordinatePixel("../classes/geography/22S48_ZN.tif", x1[i], y1[i]))
    # elevation.append(getCoordinatePixel("../classes/geography/22S48_ZN.tif", x1[i], y1[i]))
    #elevation.update((keys[i],elevation_value))
np_elevation = np.array(elevation)
pd_elevation = pd.Series(elevation,index=keys)
nx.set_node_attributes(G, pd_elevation.to_dict(), name="elevation")
ox.io.save_graphml(G, filepath='../map2.graphml')
nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma')
fig, ax = ox.plot_graph(G, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')
G = ox.add_edge_grades(G)
ox.io.save_graphml(G, filepath='../map3.graphml')
nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma')
fig1, ax1 = ox.plot_graph(G, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')


############################3
route_by_parametro = ox.shortest_path(G, a[1], a[5], weight='nome_do_parametro')

# Network x
print(G.succ if G.is_directed() else G.adj)
id_node = 32343

# get object neighbors by id node:
neighbors = G.neighbors(id_node) # lis(neighbors)

# OR
peso = _weight(G, impedance)
for v, e in G.succ[id_node].items():
    print('adjacente node:', v)
    print('characteristics', e)
    print('peso', G.edges[id_node, v, 0]['name_attribute'])
    print('peso', peso(id_node, v, e))


##################################
def heursitic():
    a = G.succ
    b = a.get(860793214)
    print(b)
    l = G.neighbors(860793214)
    print(list(l))
    coord_x = nx.get_node_attributes(G, "x")
    print(coord_x.get(860793214))
    #for v, e in G.succ[860793214].items():
        #print('adjacente node:', v)
        #print('characteristics', e)

        # print('peso', G.edges[860793214, v, 0][name_attribute])
        # funciona apenas quando o weigth retorna funcao lambda
        # print('peso', peso(860793214, v, e))