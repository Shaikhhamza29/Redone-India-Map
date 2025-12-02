# Redone-India-Map

A simple and interactive project that visualizes a redesigned map of India using HTML and Python-based preprocessing of shapefile data.  
This repository includes a browser-viewable map along with scripts to process and update geographical data.

---

## 📌 Features
- Interactive India map viewable through `index.html`
- Python script (`Redone.py`) to process shapefile/vector data
- Shapefile input folder (`in_shp/`) included for map geometry
- Additional experimental script (`try.py`)
- Sample images (`india-map.png`, `india-culture-map.webp`) for reference

---

## 📂 Project Structure
/
├── .idea/ # IDE metadata (PyCharm/IntelliJ)
├── in_shp/ # Input shapefile / vector data
├── index.html # Web page for viewing the processed map
├── Redone.py # Main Python script for map processing
├── try.py # Experimental/testing script
├── india-map.png # Sample map preview
├── india-culture-map.webp # Cultural version map preview
└── README.md # Documentation (this file)

## 🚀 Installation & Setup

### 1. Clone the repository

git clone https://github.com/Shaikhhamza29/Redone-India-Map.git

cd Redone-India-Map

### 2. Install Python dependencies
(Create a requirements.txt later if needed.)
pip install geopandas shapely matplotlib fiona


### 3. Process the shapefile data
python Redone.py


### 4. View the map
Simply open index.html in any browser

