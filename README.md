# ParSuit

ParSuit is a land suitability analysis application for the Hartford Capitol Region. It empowers users to prioritize geographic and environmental factors using simple slider adjustments to identify the most suitable parcels for their projects.

## Demo Video

Click the LINK below to watch the demo video:

![ParSuit Demo](https://drive.google.com/file/d/11UipdGlYFDdVKmQU1bRMaGJC70mI3WQa/view?usp=sharing)

## Features

- User-friendly interface with slider adjustments for various geographic and environmental factors
- Preset scenarios for quick analysis (Balanced, Urban-Intensified, Rural Favorite, Community-Based, Lone Star Ranger)
- Real-time visualization of suitability scores on a map
- Detailed glossary explaining each factor
- Integration with ArcGIS for geospatial analysis

## Requirements

- Python 3.x
- ArcGIS Pro with Spatial Analyst Extension
- Web browser (for the web viewer)

## Installation

1. Clone the repository:
 ```
git clone https://github.com/your-username/ParSuit.git
 ```
2. Install the required Python packages:
 ```
pip install -r requirements.txt
 ```
3. Set up the necessary file paths and directories in the `WeightedOverlayScript.py` file.

4. Download the APRX file from Google Drive:
- Go to the following Google Drive link: [ParSuit APRX File](https://drive.google.com/file/d/1Yl4ZrwjioPQ1v-frhyUHboVpYYmMrPD-/view?usp=sharing)
- Download the APRX file and place it in the appropriate directory referenced in the `WeightedOverlayScript.py` script.


## Usage

1. Run the `ParSuitApp.py` script to launch the ParSuit application:
 ```
python ParSuitApp.py
 ```
2. Adjust the sliders based on your preferences or select a preset scenario.

3. Click the "Process Weighted Overlay" button to generate the suitability map.

4. The web viewer will automatically open in your default web browser, displaying the suitability map and various layers.

5. Interact with the map, explore different layers, and view detailed information about parcels and points of interest.

## Folder Structure

- `ParSuitBrowser.py`: The main Python script for the ParSuit application.
- `WeightedOverlayScript.py`: The Python script for performing the weighted overlay analysis using ArcGIS.
- `script.js`: The JavaScript code for the web viewer.
- `data/`: Directory containing the generated GeoJSON files.
- `icons/`: Directory containing icons used in the application.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.