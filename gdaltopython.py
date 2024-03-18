import subprocess

def generate_tiles(input_file, output_folder):
    """
    Generate tiles from a GeoTIFF file by calling gdal2tiles.py as an external command.
    
    Args:
    input_file (str): Path to the input GeoTIFF file.
    output_folder (str): Path to the output directory for the tiles.
    """
    # Specify the path to the Python executable within the ArcGIS Pro environment
    python_executable = r'C:\Program Files\ArcGIS\Pro\bin\Python\scripts\python.exe'
    # Path to the gdal2tiles.py script
    gdal2tiles_script = r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Lib\site-packages\osgeo_utils\gdal2tiles.py'
    
    # Command to execute gdal2tiles.py through the Python interpreter
    command = [python_executable, gdal2tiles_script, '-z', '0-18', '--profile=mercator', input_file, output_folder]
    
    try:
        # Execute the command
        subprocess.run(command, check=True)
        print("Tiles generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during tile generation: {e}")

# Example usage
if __name__ == '__main__':
    input_file = r'C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\Overlay.tif'
    output_folder = r'C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\Tiles'
    generate_tiles(input_file, output_folder)
