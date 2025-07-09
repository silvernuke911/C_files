import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

def clean_name(name):
    """Handle all possible name formats from OSM data"""
    if isinstance(name, list):
        return ', '.join([str(n) for n in name if pd.notna(n)])
    elif pd.isna(name):
        return "Unnamed Road"
    return str(name)

# Define UP Diliman boundary coordinates (expanded slightly)
up_boundary = Polygon([
    (121.056, 14.641),  # SW corner (expanded)
    (121.056, 14.666),  # NW corner (expanded)
    (121.080, 14.666),  # NE corner (expanded)
    (121.080, 14.641),  # SE corner (expanded)
    (121.056, 14.641)   # Close polygon
])

# Get all roads within boundary
G = ox.graph_from_polygon(up_boundary, network_type='drive', simplify=True)
roads = ox.graph_to_gdfs(G, nodes=False)

# Process all roads
all_roads = []
for _, road in roads.iterrows():
    coords = list(road['geometry'].coords)
    all_roads.append({
        'name': clean_name(road.get('name')),
        'type': road.get('highway', 'road'),
        'length_m': int(road['length']),
        'start_coord': f"{coords[0][0]:.6f}, {coords[0][1]:.6f}",
        'end_coord': f"{coords[-1][0]:.6f}, {coords[-1][1]:.6f}"
    })

# Create DataFrame
df = pd.DataFrame(all_roads)

# Print all roads grouped by type
print("COMPLETE ROAD NETWORK IN UP DILIMAN AREA")
print("="*70)
for road_type in df['type'].sort_values().unique():
    print(f"\n{road_type.upper()}S:")
    print("-"*50)
    subset = df[df['type'] == road_type].sort_values('name')
    print(subset[['name', 'length_m', 'start_coord']].to_string(index=False))

# Save to CSV
df.to_csv("up_diliman_all_roads.csv", index=False)
print("\nFull list saved to 'up_diliman_all_roads.csv'")

# Print summary statistics
print("\nSUMMARY STATISTICS:")
print(f"Total roads: {len(df)}")
print(f"Named roads: {len(df[df['name'] != 'Unnamed Road'])}")
print(f"Road types: {', '.join(df['type'].unique())}")
print(f"Longest road: {df.loc[df['length_m'].idxmax(), 'name']} ({df['length_m'].max()}m)")