import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon

# Configure OSMnx
ox.settings.log_console = True
ox.settings.use_cache = True
ox.settings.timeout = 300  # 5 minute timeout

def get_up_diliman_map():
    try:
        # 1. Get the boundary of UP Diliman
        print("Getting UP Diliman boundary...")
        boundary = ox.geocode_to_gdf("University of the Philippines Diliman, Quezon City")
        
        # 2. Get street network within boundary
        print("Downloading street data...")
        G = ox.graph_from_polygon(boundary.geometry[0], network_type='all')
        
        # 3. Get buildings within boundary
        print("Downloading building data...")
        tags = {'building': True}
        buildings = ox.features_from_polygon(boundary.geometry[0], tags=tags)
        
        # 4. Create plot
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Plot buildings (modern method without descartes)
        buildings.plot(
            ax=ax,
            color='#6699cc',
            edgecolor='#404040',
            linewidth=0.5,
            alpha=0.6
        )
        
        # Plot streets
        ox.plot_graph(
            G,
            ax=ax,
            node_size=0,
            edge_linewidth=1,
            edge_color='#333333',
            bgcolor='none',
            show=False
        )
        
        # Add title and save
        plt.title("Sigmap v2)")
        plt.savefig(r'C:\Users\verci\Documents\code\c_files\Python\pygame_particle\sigmap_v4.png', dpi=600, bbox_inches='tight')
        print("Map saved successfully!")
        plt.show()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Upgrade packages: pip install --upgrade osmnx geopandas shapely")
        print("2. Try a smaller area or different location")
        print("3. Check your internet connection")

if __name__ == "__main__":
    get_up_diliman_map()