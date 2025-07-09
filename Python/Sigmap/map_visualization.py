print("Operation Starting")

print("Importing...")
import os
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import pickle
from matplotlib import rcParams
from JeepRoutes import get_all_routes
import labels

# Configure global font settings
plt.rcParams['font.family'] = "Consolas" # 'sans-serif'  # Base font family
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']  # Fallback fonts
plt.rcParams['font.style'] = 'normal'  # 'normal', 'italic', 'oblique'
plt.rcParams['font.weight'] = 'normal'  # 'normal', 'bold', 'light'

print("Importing Done!")

print("Loading Cache...")
# Configuration
CACHE_DIR = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\map_cache"
img_dir = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\map_imgs"
filename_base = "sigmap_v15"
file_ext = ".png"
label_streets  = False  # Set to False to disable street name labels.
label_buildings = True  
jeep_routes = True
print("Loading Done!")

# Example bounds
lat_min, lat_max = 14.647, 14.6635
lon_min, lon_max = 121.0525, 121.0762

ROUTE_STYLES = {
    "ikot": {
        "edge_color": '#FFFF00',  # Yellow
        "edge_width": 3,
        "edge_style": "-",
        "node_color": '#FFFF00',
        "node_size": 0,
        "label_color": "black"
    },
    "philcoa": {
        "edge_color": "green", #'#22B14C',  # Green
        "edge_width": 3,
        "edge_style": "-",
        "node_color": "green", #'#22B14C',
        "node_size": 0,
        "label_color": "black"
    },
    "overlap": {
        "edge_color": "#9ACD32",  # Yellow Green
        "edge_width": 3,
        "edge_style": "-",
        "node_color": "#9ACD32",
        "node_size": 0,
        "label_color": "black"
    }
}

# Loading functions
print("Loading functions...")
ox.settings.use_cache = True

def rgb_to_hex(r, g, b):
    """Convert RGB values (0–255) to hex string."""
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def handle_file_saving(directory, base_name, ext=".png"):
    """Handle the complete saving workflow after plotting."""
    while True:
        save_path = os.path.join(directory, base_name + ext)
        
        if os.path.exists(save_path):
            print(f"\nFile '{save_path}' already exists!")
            response = input("[1] Ovewrite [2] Rename [3] Cancel: ").strip().lower()
            
            if response == '1':
                return save_path
            elif response == '3':
                return None
            elif response == '2':
                new_name = input("Enter new filename (without extension): ").strip()
                if new_name:
                    base_name = new_name
                    continue
                else:
                    print("No name entered. Try again.")
            elif response == '3':
                return None
            else:
                print("Invalid option. Try again.")
        else:
            return save_path

def load_cached_data():
    """Load all data from cache."""
    try:
        with open(os.path.join(CACHE_DIR, "boundary.pkl"), 'rb') as f:
            boundary = pickle.load(f)
        G = ox.load_graphml(filepath=os.path.join(CACHE_DIR, "street_network.graphml"))
        buildings = gpd.read_file(os.path.join(CACHE_DIR, "buildings.geojson"))
        return boundary, G, buildings
    except Exception as e:
        raise RuntimeError(f"Failed to load cached data: {e}")

def in_bbox(geom, bbox):
    """Check if geometry is within bounding box."""
    lat_min, lat_max, lon_min, lon_max = bbox
    if geom.is_empty:
        return False
    minx, miny, maxx, maxy = geom.bounds
    return not (maxx < lon_min or minx > lon_max or maxy < lat_min or miny > lat_max)

def plot_map(boundary, G, buildings):
    """Plot the map with styled roads and return the figure."""
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot buildings
    print("Plotting buildings")
    bbox = (lat_min, lat_max, lon_min, lon_max)
    buildings = buildings[
        buildings.geometry.apply(lambda x: in_bbox(x, bbox)) & 
        ~buildings.geometry.geom_type.isin(['Point', 'MultiPoint'])
    ]
    
    if len(buildings) == 0:
        print("Warning: No buildings found within bounds!")
        ax.set_xlim(lon_min, lon_max)
        ax.set_ylim(lat_min, lat_max)
    else:
        buildings.plot(
            ax=ax,
            color='#6699cc',
            edgecolor='#404040',
            linewidth=0.5,
            alpha=0.6,
            zorder=1
        )

    # Plot roads
    print("Converting graph to GeoDataFrame")
    nodes, edges = ox.graph_to_gdfs(G)
    edges = edges[edges.geometry.apply(lambda x: in_bbox(x, bbox))]
    edges['highway'] = edges['highway'].astype(str)

    road_styles = {
        'primary':      {'width': 5, 'color': rgb_to_hex(30,30,30)},
        'secondary':    {'width': 4, 'color': rgb_to_hex(50,50,50)},
        'tertiary':     {'width': 4, 'color': rgb_to_hex(80,80,80)},
        'unclassified': {'width': 3, 'color': rgb_to_hex(80,80,80)},
        'minor':        {'width': 2, 'color': rgb_to_hex(100,100,100)},
    }

    for key, style in road_styles.items():
        if key == 'minor':
            road_subset = edges[~edges['highway'].str.contains('primary|secondary|tertiary|unclassified', case=False, na=False)]
        else:
            road_subset = edges[edges['highway'].str.contains(key, case=False, na=False)]
        
        if not road_subset.empty:
            road_subset.plot(
                ax=ax,
                linewidth=style['width'],
                edgecolor=style['color'],
                alpha=0.95,
                zorder=2 if key == 'minor' else 3
            )

    # Plot custom routes
    if jeep_routes:
        print("Plotting Jeep Routes")
        custom_routes = get_all_routes()
        for route_name, route_graph in custom_routes.items():
            style = ROUTE_STYLES.get(route_name, {})
            nodes, edges = ox.graph_to_gdfs(route_graph)
            
            edges.plot(
                ax=ax,
                linewidth=style.get("edge_width", 2),
                edgecolor=style.get("edge_color", "#000000"),
                linestyle=style.get("edge_style", "-"),
                alpha=0.9,
                zorder=4
            )
            
            nodes.plot(
                ax=ax,
                color=style.get("node_color", "#000000"),
                markersize=style.get("node_size", 30),
                zorder=5
            )

    if label_streets:
        for label in labels.STREET_LABELS:
            ax.text(
                label["x"], label["y"],
                label["name"],
                rotation=label.get("rotation", 0),
                fontsize=label.get("fontsize", 8),
                color=label.get("color", "black"),
                ha='center',
                va='center',
                bbox=label.get("bbox", None),
                zorder=10  # Ensure labels appear on top
            )
    
    # Add manual building labels
    if label_buildings:
        for label in labels.BUILDING_LABELS:
            ax.text(
                label["x"], label["y"],
                label["name"],
                rotation=label.get("rotation", 0),
                fontsize=label.get("fontsize", 7),
                color=label.get("color", "black"),
                ha='center',
                va='center',
                bbox=label.get("bbox", None),
                zorder=10
            )
    
    ## BACKGROUND COLOR
    fig.patch.set_facecolor("#FFFFFF")         # Set figure background
    ax.set_facecolor('#FFFFFF') 

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(lon_min, lon_max)
    plt.ylim(lat_min, lat_max)
    # plt.title(f"{filename_base}")
    plt.axis(False)

    # Ask to save after displaying
    save_choice = input("Save image? [Y/N]: ").strip().lower()
    if save_choice in ['y', "1"]:
        save_path = handle_file_saving(img_dir, filename_base, file_ext)
        if save_path:
            fig.savefig(save_path, dpi=700, bbox_inches='tight')
            print(f"Map saved to '{save_path}'")
        else:
            print("Save cancelled.")
    else:
        print("Image not saved.")
    return fig

print("Loading functions Done!")

def main():
    try:
        print("Loading data from cache...")
        boundary, G, buildings = load_cached_data()

        print("Generating plot...")
        fig = plot_map(boundary, G, buildings)
        plt.show()  # Show the plot first

        

        print("Operation Complete!")

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify cache files exist and are valid")
        print("2. Check coordinate ranges are valid")
        print("3. Ensure output directory exists")

if __name__ == "__main__":
    main()