# **AID: Adaptive Image-Data Index for Interactive Multilevel Visualization**

## **Project Overview**

This repository contains the implementation of the **Adaptive Image-Data (AID) index** for big spatial data visualization. The AID index combines image tiles and data tiles to efficiently visualize large datasets while maintaining interactivity. This project replicates the core concepts from the paper "**AID: An Adaptive Image Data Index for Interactive Multilevel Visualization**" and provides a Python-based implementation that includes:

- **Tile generation** based on data density.
- **Flask server** to serve tiles dynamically.
- **Frontend** to visualize the data interactively with zoom and pan functionality.

### **Key Features**
- Adaptive index combining **image tiles** for dense data and **data tiles** for sparse regions.
- Dynamically generated tiles for user interactions.
- Scalable solution for big spatial data visualization.

---

## **Project Setup**

Follow these steps to set up and run the project on your local machine.

### **1. Prerequisites**

Before getting started, ensure that you have the following installed:

- **Python 3.7+**
- **pip** (Python package installer)
- **Git** (to clone the repository)

### **2. Clone the Repository**

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/aid-index-visualization.git
cd aid-index-visualization
```

### **3. Install Required Libraries**

Install the necessary Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### **4. Generate the Synthetic Dataset**

This project generates a synthetic dataset to simulate spatial data for the experiment. The dataset is created using `numpy` and `pandas`.

Run the dataset generation script:

```bash
python aid_index_construction.py
```

This will create a synthetic dataset saved as `synthetic_spatial_data.csv` and generate tiles stored in the `output/` directory.

### **5. Run the Flask Server**

Once the dataset is ready, run the Flask server to serve the tiles dynamically. The server will handle requests for both image tiles and dynamically generated data tiles.

Start the Flask server:

```bash
python visualization_server.py
```

By default, the server will run on `http://localhost:5000/`.

### **6. Visualize the Data**

To interact with the visualization, open the `index.html` file in your browser. You can also serve the HTML file through a simple HTTP server:

```bash
python -m http.server 8000
```

Visit `http://localhost:8000/index.html` in your browser to see the interactive visualization in action.

---

## **Project Structure**

```
aid-index-visualization/
│
├── aid_index_construction.py   # Dataset generation and AID index construction
├── visualization_server.py     # Flask server to serve tiles
├── index.html                  # Frontend visualization
├── requirements.txt            # List of required Python libraries
├── synthetic_spatial_data.csv  # Generated synthetic dataset
├── output/                     # Folder containing image and data tiles
│   ├── image_tiles/            # Pregenerated image tiles
│   └── data_tiles/             # Raw data tiles
```

---

## **Usage**

### **Dataset**

The synthetic dataset is generated based on spatial data points with a value attribute. The script `aid_index_construction.py` allows you to generate this dataset and classify it into **image tiles** and **data tiles**. 

### **Frontend**

The interactive visualization allows you to zoom in, zoom out, and pan across the map, which dynamically fetches the necessary tiles from the Flask server. Tiles are requested based on zoom levels and coordinates, and missing tiles are generated on demand from the raw data.

### **Serving the Project**

You can serve the project by running the Flask server and opening the HTML file in your browser. The server will fetch tiles from the `output/image_tiles` or generate them dynamically from the `output/data_tiles` as needed.

---

## **Contributing**

If you'd like to contribute to this project, feel free to fork the repository, create a branch, and submit a pull request. You can improve the project by adding features, fixing bugs, or optimizing performance.

### **How to Contribute**:
1. Fork this repository.
2. Clone your fork to your local machine.
3. Create a new branch (`git checkout -b feature-branch`).
4. Make your changes and commit them (`git commit -am 'Add new feature'`).
5. Push to your branch (`git push origin feature-branch`).
6. Create a pull request to the main repository.

---

## **Acknowledgments**

- The original **AID index** paper: *"AID: An Adaptive Image Data Index for Interactive Multilevel Visualization"*.
- All contributors to this project.
