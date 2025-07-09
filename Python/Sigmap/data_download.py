import osmnx as ox
import geopandas as gpd
import pickle
import os

# Configure cache location
CACHE_DIR = r"C:\Users\verci\Documents\code\c_files\Python\Sigmap\map_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def download_and_cache_data():
    # Define UP Diliman area
    place = "University of the Philippines Diliman, Quezon City, Philippines"
    
    print("Downloading boundary...")
    boundary = ox.geocode_to_gdf(place)
    with open(f"{CACHE_DIR}/boundary.pkl", 'wb') as f:
        pickle.dump(boundary, f)
    
    print("Downloading street network...")
    G = ox.graph_from_polygon(boundary.geometry[0], network_type='all')
    ox.save_graphml(G, filepath=f"{CACHE_DIR}/street_network.graphml")
    
    print("Downloading buildings...")
    tags = {'building': True}
    buildings = ox.features_from_polygon(boundary.geometry[0], tags=tags)
    buildings.to_file(f"{CACHE_DIR}/buildings.geojson", driver='GeoJSON')
    
    print("All data downloaded and cached!")

if __name__ == "__main__":
    download_and_cache_data()