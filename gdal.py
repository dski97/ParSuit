import os
from osgeo import gdal
import numpy as np

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

# Open the raster file
input_file = r'C:\Users\cwalinskid\Downloads\ParSuit\ParSuit\ParSuit\Overlay.tif'
if os.path.exists(input_file):
    dataset = gdal.Open(input_file)
    if dataset is None:
        print(f"Failed to open raster file: {input_file}")
    else:
        print(f"Raster file opened successfully: {input_file}")
else:
    print(f"Raster file does not exist: {input_file}")
    exit(1)

# Create the output directory for tiles
output_directory = r'C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit'
create_directory(output_directory)

zoom_levels = [8, 9, 10, 11, 12]  # Adjust zoom levels as needed

# Get the geotransform and calculate the extent
geotransform = dataset.GetGeoTransform()
print(f"Geotransform: {geotransform}")

x_min = geotransform[0]
y_max = geotransform[3]
x_max = x_min + geotransform[1] * dataset.RasterXSize
y_min = y_max + geotransform[5] * dataset.RasterYSize
x_res = geotransform[1]
y_res = geotransform[5]

print(f"Raster extent: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")
print(f"Raster resolution: x_res={x_res}, y_res={y_res}")

# Create a dictionary mapping unique values to colors
colorizer = {
    0: (165, 0, 38),
    3: (244, 109, 67),
    7: (254, 224, 139),
    8: (217, 239, 139),
    9: (102, 189, 99),
    10: (0, 104, 55)
}

# Generate tiles
driver = gdal.GetDriverByName('GTiff')
for zoom in zoom_levels:
    zoom_directory = os.path.join(output_directory, str(zoom))
    create_directory(zoom_directory)

    tile_size = 256  # Tile size in pixels
    
    tile_min_x = int((x_min - geotransform[0]) / (tile_size * geotransform[1]))
    tile_max_x = int((x_max - geotransform[0]) / (tile_size * geotransform[1])) + 1
    tile_min_y = int((y_max - geotransform[3]) / (tile_size * geotransform[5]))
    tile_max_y = int((y_min - geotransform[3]) / (tile_size * geotransform[5])) + 1
    
    for i in range(tile_min_x, tile_max_x):
        for j in range(tile_min_y, tile_max_y):
            x_offset = int((geotransform[0] + i * tile_size * geotransform[1] - x_min) / geotransform[1])
            y_offset = int((geotransform[3] + j * tile_size * geotransform[5] - y_max) / -geotransform[5])
            
            print(f"Zoom: {zoom}, i: {i}, j: {j}, x_offset: {x_offset}, y_offset: {y_offset}")
            
            # Check if the tile extent is within the raster's bounds
            if x_offset >= 0 and y_offset >= 0 and x_offset + tile_size <= dataset.RasterXSize and y_offset + tile_size <= dataset.RasterYSize:
                # Create the tile
                tile_path = os.path.join(zoom_directory, str(i), f"{j}.tif")
                tile_directory = os.path.dirname(tile_path)
                create_directory(tile_directory)
                
                tile_dataset = driver.Create(tile_path, tile_size, tile_size, 3, gdal.GDT_Byte)
                
                # Set the tile's geotransform
                tile_geotransform = (geotransform[0] + i * tile_size * geotransform[1],
                                     geotransform[1], 0,
                                     geotransform[3] + j * tile_size * geotransform[5],
                                     0, geotransform[5])
                tile_dataset.SetGeoTransform(tile_geotransform)
                
                # Write the tile data
                tile_data = dataset.ReadAsArray(x_offset, y_offset, tile_size, tile_size)
                
                # Apply the colorizer to the tile data
                tile_data_rgb = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)
                for value, color in colorizer.items():
                    mask = (tile_data == value)
                    tile_data_rgb[mask] = color
                
                # Write the RGB tile data
                tile_dataset.GetRasterBand(1).WriteArray(tile_data_rgb[..., 0])
                tile_dataset.GetRasterBand(2).WriteArray(tile_data_rgb[..., 1])
                tile_dataset.GetRasterBand(3).WriteArray(tile_data_rgb[..., 2])
                
                # Close the tile dataset
                tile_dataset = None
                
                print(f"Created tile: {tile_path}")
            else:
                print(f"Skipping tile: Zoom: {zoom}, i: {i}, j: {j} (out of bounds)")

# Close the input dataset
dataset = None

print("Tile generation completed.")