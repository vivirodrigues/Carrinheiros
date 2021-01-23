import osmnx as ox

# lat-lon -22.796008, -22.843953, -47.054891, -47.107718000000006
G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
G_projected = ox.project_graph(G)
ox.io.save_graphml(G, filepath='../map.graphml')
ox.plot_graph(G_projected)