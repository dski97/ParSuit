import arcpy
from arcpy.sa import *

# Define the input raster
input_raster = r"C:\Users\Dominic\Desktop\ParSuitAPRX\landuse.gdb\landuse"

# Define the remap object
remapLanduse = RemapValue([
    ["Impervious Surfaces", 9],
    ["Developed Open Space", 8],
    ["Cultivated Land", 8],
    ["Pasture/Hay", 8],
    ["Grassland", 8],
    ["Mixed Forest", 7],
    ["Scrub/Shrub", 7],
    ["Palustrine Forested Wetland", 3],
    ["Palustrine Scrub/Shrub Wetland", 3],
    ["Palustrine Emergent Wetland", 3],
    ["Estuarine Emergent Wetland", 3],
    ["Unconsolidated Shore", 3],
    ["Bare Land", 10],
    ["Open Water", "Restricted"],
    ["Palustrine Aquatic Bed", "Restricted"],
    ["''", "NODATA"],
    ["NODATA", "NODATA"]
])

# Perform the reclassification
reclassified_raster = arcpy.sa.Reclassify(input_raster, "Value", remapLanduse)

# Save the reclassified raster
output_raster = r"C:\Users\Dominic\Desktop\ParSuitAPRX\ParSuit.gdb\reclassified_landuse"
reclassified_raster.save(output_raster)