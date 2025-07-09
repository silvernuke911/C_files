import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib import rcParams

# Configure OSMnx
ox.settings.log_console = True
ox.settings.use_cache = True
ox.settings.timeout = 300

def get_up_diliman_map_with_labels():
    try:
        # 1. Get boundary
        print("Getting boundary...")
        boundary = ox.geocode_to_gdf("University of the Philippines Diliman, Quezon City")
        
        # 2. Get graph with all edge attributes
        print("Downloading street data...")
        G = ox.graph_from_polygon(boundary.geometry[0], network_type='all', retain_all=True)
        
        # 3. Get buildings
        print("Downloading buildings...")
        tags = {'building': True}
        buildings = ox.features_from_polygon(boundary.geometry[0], tags=tags)
        
        # 4. Prepare plot
        fig, ax = plt.subplots(figsize=(15, 15))
        
        # 5. Plot buildings
        buildings.plot(ax=ax, color='#6699cc', edgecolor='#404040', alpha=0.6, linewidth=0.5)
        
        # 6. Plot streets with labels
        print("Processing street labels...")
        
        # Get edge geometries and names
        edges = ox.graph_to_gdfs(G, nodes=False)
        edges = edges[edges.geometry.notnull() & edges['name'].notnull()]
        
        # Plot each labeled street
        for _, edge in edges.iterrows():
            # Plot street line
            x, y = edge.geometry.xy
            ax.plot(x, y, color='#333333', linewidth=1, zorder=1)
            
            # Add label at midpoint
            midpoint = edge.geometry.interpolate(0.5, normalized=True)
            ax.text(
                midpoint.x, midpoint.y,
                edge['name'],
                fontsize=8,
                ha='center',
                va='center',
                color='black',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'),
                rotation=45 if len(str(edge['name'])) > 15 else 0,
                zorder=2,
                fontfamily='sans-serif'  # Use system default sans-serif font
            )
        
        # 7. Customize plot
        plt.title("UP Diliman Campus Map with Street Names", fontsize=16)
        ax.set_axis_off()
        plt.tight_layout()
        
        # 8. Save and show
        plt.savefig('up_diliman_streets_labeled.png', dpi=300, bbox_inches='tight')
        print("Map saved successfully!")
        plt.show()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Try smaller area with ox.features_from_address()")
        print("3. Upgrade packages: pip install --upgrade osmnx geopandas")

if __name__ == "__main__":
    # Use system default font without file dependency
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']  # Fallback options
    
    get_up_diliman_map_with_labels()