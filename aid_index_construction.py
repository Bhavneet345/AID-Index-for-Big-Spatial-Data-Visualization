import os
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Constants
ZOOM_LEVELS = 4  # Number of zoom levels (0 to 3)
TILE_SIZE = 256  # Size of each tile in pixels
THRESHOLD = 100  # Threshold to classify tiles as image or data

# Directories for outputs
os.makedirs("output/image_tiles", exist_ok=True)
os.makedirs("output/data_tiles", exist_ok=True)

# Step 1: Generate Synthetic Dataset
def create_synthetic_dataset(num_clusters=5, cluster_size=2000, sparse_points=10000, x_range=(0, 10000), y_range=(0, 10000)):
    """Generate synthetic dataset with clustered and sparse spatial data."""
    np.random.seed(42)  # For reproducibility
    cluster_centers = np.random.uniform(x_range[0], x_range[1], size=(num_clusters, 2))
    cluster_data = []
    for center in cluster_centers:
        x_center, y_center = center
        x_vals = np.random.normal(x_center, scale=500, size=cluster_size)
        y_vals = np.random.normal(y_center, scale=500, size=cluster_size)
        values = np.random.randint(50, 100, cluster_size)  # High intensity
        cluster_data.append(pd.DataFrame({'x': x_vals, 'y': y_vals, 'value': values}))

    clustered_data = pd.concat(cluster_data, ignore_index=True)
    sparse_x = np.random.uniform(x_range[0], x_range[1], sparse_points)
    sparse_y = np.random.uniform(y_range[0], y_range[1], sparse_points)
    sparse_values = np.random.randint(1, 50, sparse_points)  # Low intensity
    sparse_data = pd.DataFrame({'x': sparse_x, 'y': sparse_y, 'value': sparse_values})
    combined_data = pd.concat([clustered_data, sparse_data], ignore_index=True)
    return combined_data

# Step 2: Generate Tile IDs
def generate_tile_id(x, y, zoom):
    """Generate a unique tile ID based on coordinates and zoom level."""
    scale = TILE_SIZE * (2 ** zoom)
    return f"{zoom}_{int(x // scale)}_{int(y // scale)}"

# Step 3: Construct the AID Index
def construct_aid_index(data, zoom_levels, threshold):
    """Construct the AID index by classifying tiles as image or data."""
    for zoom in range(zoom_levels):
        print(f"Processing Zoom Level {zoom}...")
        data['tile_id'] = data.apply(lambda row: generate_tile_id(row['x'], row['y'], zoom), axis=1)
        tile_groups = data.groupby('tile_id')

        for tile_id, group in tile_groups:
            if len(group) > threshold:
                create_image_tile(tile_id, group)
            else:
                save_data_tile(tile_id, group)

def create_image_tile(tile_id, group):
    """Generate and save an image tile."""
    img = Image.new('RGB', (TILE_SIZE, TILE_SIZE), color='white')
    draw = ImageDraw.Draw(img)
    for _, row in group.iterrows():
        x, y = int(row['x'] % TILE_SIZE), int(row['y'] % TILE_SIZE)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='blue')
    img.save(f"output/image_tiles/{tile_id}.png")
    print(f"Saved image tile: {tile_id}")

def save_data_tile(tile_id, group):
    """Save data tile as a CSV file."""
    output_path = f"output/data_tiles/{tile_id}.csv"
    group.to_csv(output_path, index=False)
    print(f"Saved data tile: {tile_id}")

# Step 4: Visualize the Dataset
def plot_dataset(data, title="Synthetic Spatial Dataset"):
    """Plot the synthetic dataset for visualization."""
    plt.figure(figsize=(10, 8))
    plt.scatter(data['x'], data['y'], c=data['value'], cmap='viridis', s=10, alpha=0.7)
    plt.colorbar(label='Value (Intensity)')
    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.show()

# Main Execution
if __name__ == "__main__":
    # Generate synthetic dataset
    synthetic_data = create_synthetic_dataset()
    synthetic_data.to_csv("synthetic_spatial_data.csv", index=False)
    print("Synthetic dataset saved to 'synthetic_spatial_data.csv'.")
    
    # Visualize synthetic dataset
    plot_dataset(synthetic_data)
    
    # Construct AID index
    construct_aid_index(synthetic_data, ZOOM_LEVELS, THRESHOLD)
    print("AID Index Construction Completed!")
