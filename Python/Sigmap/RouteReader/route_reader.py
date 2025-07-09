from xml.etree import ElementTree as ET
import networkx as nx
from geopy.distance import geodesic

ikot_input_file = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\RouteReader\IkotRoute.kml"

def get_kml_coords(kml_path):
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    tree = ET.parse(kml_path)
    root = tree.getroot()

    coords = []
    for linestring in root.findall('.//kml:LineString', ns):
        coord_text = linestring.find('kml:coordinates', ns).text.strip()
        for line in coord_text.split():
            lon, lat, *_ = line.split(',')
            coords.append((float(lat), float(lon)))
    return coords

ikot_route_coords = get_kml_coords(ikot_input_file)

for i, coord in enumerate (ikot_route_coords):
    print(f"({i},{coord[0]},{coord[1]},'node{i}'),")

G = nx.MultiDiGraph(crs="EPSG:4326")

# Add nodes
for i, (lat, lon) in enumerate(ikot_route_coords):
    G.add_node(i, y=lat, x=lon, name=f"node{i}")

# Add edges with geodesic length
for i in range(len(ikot_route_coords) - 1):
    point1 = ikot_route_coords[i]
    point2 = ikot_route_coords[i + 1]
    distance_m = geodesic(point1, point2).meters
    G.add_edge(i, i + 1, length=distance_m, name="IKOT ROUTE")

# print(list(G.nodes(data=True)))
# print(list(G.edges(data=True)))
for i in list(G.edges(data=True)):
    print(i)

output_file = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\RouteReader\ikot_route_nodes.txt"

with open(output_file, 'w') as f:
    f.write("NODES\n")
    for i, (lat, lon) in enumerate(ikot_route_coords):
        f.write(f"({i},{lat},{lon},'node{i}'),\n")
    f.write("EDGES\n")
    for i in list(G.edges(data=True)):
        f.write(f"{i},\n")


philcoa_input_file = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\RouteReader\PhilcoaRoute.kml"

philcoa_route_coords = get_kml_coords(philcoa_input_file)

for i, coord in enumerate (philcoa_route_coords):
    print(f"({i},{coord[0]},{coord[1]},'node{i}'),")

G = nx.MultiDiGraph(crs="EPSG:4326")

# Add nodes
for i, (lat, lon) in enumerate(philcoa_route_coords):
    G.add_node(i, y=lat, x=lon, name=f"node{i}")

# Add edges with geodesic length
for i in range(len(philcoa_route_coords) - 1):
    point1 = philcoa_route_coords[i]
    point2 = philcoa_route_coords[i + 1]
    distance_m = geodesic(point1, point2).meters
    G.add_edge(i, i + 1, length=distance_m, name="philcoa ROUTE")

# print(list(G.nodes(data=True)))
# print(list(G.edges(data=True)))
for i in list(G.edges(data=True)):
    print(i)

output_file = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\RouteReader\philcoa_route_nodes.txt"

with open(output_file, 'w') as f:
    f.write("NODES\n")
    for i, (lat, lon) in enumerate(philcoa_route_coords):
        f.write(f"({i},{lat},{lon},'node{i}'),\n")
    f.write("EDGES\n")
    for i in list(G.edges(data=True)):
        f.write(f"{i},\n")
