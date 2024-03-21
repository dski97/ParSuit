# Name: CustomWeightedOverlay.py
# Description: Overlays several rasters using a common scale and weighing
#    each according to its importance for park suitability analysis.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy.sa import *

# Check out the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Set environment settings
arcpy.env.workspace = r"C:\Users\cwalinskid\Desktop\ParSuit"
arcpy.env.cellSize = 100
arcpy.env.scratchWorkspace = r"C:\Users\cwalinskid\Desktop\ParSuit\ParSuit.gdb"

# Define local variables for the input rasters and their remap values
landuseRaster = r"C:\Users\cwalinskid\Desktop\ParSuit\landuse.gdb\landuse"
slopeRaster = r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Slope.tif"

# Define remap values for each input raster
remapLanduse = RemapValue([
    ['Impervious Surfaces', 1], 
    ['Developed Open Space', 2], 
    ['Cultivated Land', 3], 
    ['Pasture/Hay', 4], 
    ['Grassland', 5], 
    ['Mixed Forest', 6], 
    ['Scrub/Shrub', 7], 
    ['Palustrine Forested Wetland', 8], 
    ['Palustrine Scrub/Shrub Wetland', 9], 
    ['Palustrine Emergent Wetland', 1], 
    ['Estuarine Emergent Wetland', 1], 
    ['Unconsolidated Shore', 1], 
    ['Bare Land', 1], 
    ['Open Water', 1], 
    ['Palustrine Aquatic Bed', 1], 
    ['NODATA', 'NODATA']
])

remapSlope = RemapRange([
    [1, 1, 1], 
    [2, 2, 2], 
    [3, 3, 3], 
    [4, 4, 4], 
    [5, 5, 5], 
    [6, 6, 6], 
    [7, 7, 7], 
    [8, 8, 8], 
    [9, 9, 9], 
    [10, 10, 1], 
    ['NODATA', 'NODATA']
])

# Create a Weighted Overlay Table object
myWOTable = WOTable([
    [landuseRaster, 50, "VALUE", remapLanduse],
    [slopeRaster, 50, "VALUE", remapSlope]
], [1, 9, 1])

# Execute WeightedOverlay
outWeightedOverlay = WeightedOverlay(myWOTable)

# Save the output
outWeightedOverlay.save(r"C:\Users\cwalinskid\Desktop\ParSuit\ParSuit.gdb\Weightedland1")
