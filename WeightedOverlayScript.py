# Name: WeightedOverlayScript.py
# Description: Overlays several rasters using a common scale and weighing
#              each according to its importance.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import shutil
import os


# Set the base directory for input files
input_base_dir = r"C:\Users\cwalinskid\Desktop\ParSuitAPRX"

# Set the output directory for the final GeoJSON file
output_base_dir = r"C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\data"

# Slider directory
slider_dir = r"C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit"

# Set environment settings
arcpy.env.cellSize = 100
arcpy.env.scratchWorkspace = input_base_dir
arcpy.env.overwriteOutput = True

# Set local variables
inRaster1 = os.path.join(input_base_dir, "Reclass_Brownfield.tif")
inRaster2 = os.path.join(input_base_dir, "Reclass_BuildableSoil.tif")
inRaster3 = os.path.join(input_base_dir, "Reclass_Floodzones.tif")
inRaster4 = os.path.join(input_base_dir, "Reclass_Hospitals.tif")
inRaster5 = os.path.join(input_base_dir, "Reclass_PoliceCommunity.tif")
inRaster6 = os.path.join(input_base_dir, "Reclass_Roads.tif")
inRaster7 = os.path.join(input_base_dir, "Reclass_Schools.tif")
inRaster8 = os.path.join(input_base_dir, "Reclass_SewerCon.tif")
inRaster9 = os.path.join(input_base_dir, "Reclass_Slope.tif")
inRaster10 = os.path.join(input_base_dir, "Reclass_Wetlands.tif")
inRaster11 = os.path.join(input_base_dir, "landuse.gdb", "landuse")

# Remap values (unchanged)
remapBrownfield = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [
                             7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapBuildableSoil = RemapValue([[1, 3], [2, 4], [3, 5], [4, 5], [5, 5], [6, 6], [
                                7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapFloodzones = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [
                             7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapHospitals = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [
                            7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapPoliceCommunity = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [
                                  6, 6], [7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapRoads = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [
                        7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapSchools = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [
                          7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapSewerCon = RemapValue([[1, 1], [2, 1], [3, 1], [4, 1], [5, 5], [6, 6], [
                           7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapSlope = RemapValue([[1, 1], [2, 1], [3, 1], [4, 3], [5, 3], [6, 5], [
                        7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapWetlands = RemapValue([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [
                           7, 7], [8, 8], [9, 9], [10, 10], ["NODATA", "NODATA"]])
remapLanduse = RemapValue([
    [0, "NODATA"],
    [2, 9],
    [5, 8],
    [6, 8],
    [7, 8],
    [8, 8],
    [11, 7],
    [12, 7],
    [13, 3],
    [14, 3],
    [15, 3],
    [18, 3],
    [19, 3],
    [20, 10],
    [21, "Restricted"],
    [22, "Restricted"],
    ["NODATA", "NODATA"]
])

# Read slider values from the file
slider_values_path = os.path.join(slider_dir, "slider_values.txt")
with open(slider_values_path, "r") as file:
    slider_values = [int(value) for value in file.read().split(",")]

# Update the weights in the WOTable based on the slider values
myWOTable = WOTable([
    [inRaster1, slider_values[0], "VALUE", remapBrownfield],
    [inRaster2, slider_values[1], "VALUE", remapBuildableSoil],
    [inRaster3, slider_values[2], "VALUE", remapFloodzones],
    [inRaster4, slider_values[3], "VALUE", remapHospitals],
    [inRaster5, slider_values[4], "VALUE", remapPoliceCommunity],
    [inRaster6, slider_values[5], "VALUE", remapRoads],
    [inRaster7, slider_values[6], "VALUE", remapSchools],
    [inRaster8, slider_values[7], "VALUE", remapSewerCon],
    [inRaster9, slider_values[8], "VALUE", remapSlope],
    [inRaster10, slider_values[9], "VALUE", remapWetlands],
    [inRaster11, slider_values[10], "VALUE", remapLanduse]
], [1, 10, 1])

# Execute WeightedOverlay
outWeightedOverlay = WeightedOverlay(myWOTable)


# Save the output
output_path = os.path.join(input_base_dir, "output.tif")

outWeightedOverlay.save(output_path)

print("Weighted Overlay completed successfully!")

# Convert output raster to polygon
raster_polygon_path = os.path.join(input_base_dir, "raster_polygon.shp")
arcpy.RasterToPolygon_conversion(
    outWeightedOverlay, raster_polygon_path, "NO_SIMPLIFY", "VALUE")
print("Raster to Polygon completed successfully!")

# Dissolve output polygon based on the gridcode field
dissolved_polygon_path = os.path.join(input_base_dir, "dissolved_polygon.shp")
arcpy.Dissolve_management(
    raster_polygon_path, dissolved_polygon_path, "gridcode", "", "MULTI_PART")
print("Dissolve completed successfully!")

# Convert dissolved polygon to geojson
geojson_path = os.path.join(input_base_dir, "WeightedOverlay.geojson")
arcpy.FeaturesToJSON_conversion(dissolved_polygon_path, geojson_path, "FORMATTED",
                                "NO_Z_VALUES", "NO_M_VALUES", "GEOJSON", "WGS84", "USE_FIELD_NAME")
print("Conversion to GeoJSON completed successfully!")

# Move the geojson file to the ParSuit Data folder and rename it to RasterOverlay.geojson
final_geojson_path = os.path.join(output_base_dir, "RasterOverlay.geojson")
shutil.move(geojson_path, final_geojson_path, copy_function=shutil.copy2)
print("GeoJSON file moved successfully!")
