from osgeo import gdal

# Open the raster file
input_file = r'C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\Overlay.tif'
dataset = gdal.Open(input_file)

# Create the output directory for tiles
output_directory = r'C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit'
zoom_levels = [8, 9, 10, 11, 12]  # Adjust zoom levels as needed

# Get the geotransform and calculate the extent
geotransform = dataset.GetGeoTransform()
x_min = geotransform[0]
y_max = geotransform[3]
x_max = x_min + geotransform[1] * dataset.RasterXSize
y_min = y_max + geotransform[5] * dataset.RasterYSize
x_res = geotransform[1]
y_res = geotransform[5]

# Generate tiles
driver = gdal.GetDriverByName('PNG')
for zoom in zoom_levels:
    tile_size = 256  # Tile size in pixels
    
    for i in range(int((x_max - x_min) / (tile_size * x_res))):
        for j in range(int((y_max - y_min) / (tile_size * y_res))):
            x_offset = int(i * tile_size * x_res / x_res)
            y_offset = int(j * tile_size * y_res / y_res)
            
            # Create the tile
            tile_dataset = driver.Create(f'{output_directory}/{zoom}/{i}/{j}.png',
                                         tile_size, tile_size, 1, gdal.GDT_Byte)
            
            # Set the tile's geotransform
            tile_geotransform = (x_min + i * tile_size * x_res,
                                 x_res, 0,
                                 y_max + j * tile_size * y_res,
                                 0, y_res)
            tile_dataset.SetGeoTransform(tile_geotransform)
            
            # Write the tile data
            tile_data = dataset.ReadAsArray(x_offset, y_offset, tile_size, tile_size)
            tile_dataset.GetRasterBand(1).WriteArray(tile_data)
            
            # Close the tile dataset
            tile_dataset = None

# Close the input dataset
dataset = None

print("Tiles generated successfully!")