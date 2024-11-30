from flask import Flask, send_file, abort
import pandas as pd
from PIL import Image, ImageDraw
import os

app = Flask(__name__)

# Configuration
TILE_SIZE = 256
IMAGE_TILE_PATH = "output/image_tiles"
DATA_TILE_PATH = "output/data_tiles"

def generate_image_from_data(tile_id):
    """Generate an image dynamically from a data tile."""
    data_tile_path = os.path.join(DATA_TILE_PATH, f"{tile_id}.csv")
    if not os.path.exists(data_tile_path):
        return None

    # Load data tile
    data = pd.read_csv(data_tile_path)

    # Create an image
    img = Image.new('RGB', (TILE_SIZE, TILE_SIZE), color='white')
    draw = ImageDraw.Draw(img)
    for _, row in data.iterrows():
        x = int(row['x'] % TILE_SIZE)
        y = int(row['y'] % TILE_SIZE)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='blue')

    # Save the dynamically generated image for reuse
    img_path = os.path.join(IMAGE_TILE_PATH, f"{tile_id}.png")
    img.save(img_path)
    return img_path

@app.route('/tile/<int:zoom>/<int:x>/<int:y>')
def get_tile(zoom, x, y):
    """Serve a tile for a given zoom level and coordinates."""
    tile_id = f"{zoom}_{x}_{y}"
    image_path = os.path.join(IMAGE_TILE_PATH, f"{tile_id}.png")

    if os.path.exists(image_path):
        # Return pregenerated image tile
        return send_file(image_path, mimetype='image/png')
    else:
        # Generate image from data tile if it exists
        generated_image = generate_image_from_data(tile_id)
        if generated_image:
            return send_file(generated_image, mimetype='image/png')
        else:
            # Tile not found
            abort(404, description="Tile not found")

if __name__ == "__main__":
    # Ensure output directories exist
    os.makedirs(IMAGE_TILE_PATH, exist_ok=True)
    os.makedirs(DATA_TILE_PATH, exist_ok=True)
    
    # Run the server
    print("Starting the visualization server...")
    app.run(host="0.0.0.0", port=3000, debug=False)

