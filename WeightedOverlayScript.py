#import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

#set environment settings
env.workspace = r"C:\Users\Dominic\Desktop\ParsuitAPX\ParSuit"
env.overwriteOutput = True

# Set local variables for the TIFF raster files
brownfields = "Reclass_Brownfield.tif"
buildable_soil = "Reclass_BuildableSoil.tif"
floodzones = "Reclass_Floodzones.tif"
hospitals = "Reclass_Hospitals.tif"
police_community = "Reclass_PoliceCommunity.tif"
roads = "Reclass_Roads.tif"
schools = "Reclass_Schools.tif"
sewercon = "Reclass_SewerCon.tif"
slope = "Reclass_Slope.tif"
wetlands = "Reclass_Wetlands.tif"
landuse = "landuse.tif"

# RemapValue objects for each raster, based on your specifications
remap_brownfield = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_buildableSoil = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_floodzones = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_hospitals = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_policeCommunity = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_roads = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_schools = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_sewerCon = RemapValue([(1, 1), (2, 1), (3, 1), (4, 1), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_slope = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_wetlands = RemapValue([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("NODATA", "NODATA")])
remap_landuse = RemapValue([
    ("Impervious Surfaces", 9),
    ("Developed Open Space", 9),
    ("Cultivated Land", 8),
    ("Pasture/Hay", 8),
    ("Grassland", 8),
    ("Mixed Forest", 7),
    ("Scrub/Shrub", 7),
    ("Palustrine Forested Wetland", 3),
    ("Palustrine Scrub/Shrub Wetland", 3),
    ("Palustrine Emergent Wetland", 3),
    ("Estuarine Emergent Wetland", 3),
    ("Unconsolidated Shore", 3),
    ("Bare Land", 10),
    ("Open Water", "Restricted"), 
    ("Palustrine Aquatic Bed", "Restricted"), 
    ("", "NODATA"), 
    ("NODATA", "NODATA")
])

# Create a Weighted Overlay table for the TIFF raster files
myWOTable = WOTable([
    ["Reclass_Brownfield.tif", 9, "VALUE", remap_brownfield],
    ["Reclass_BuildableSoil.tif", 9, "VALUE", remap_buildableSoil],
    ["Reclass_Floodzones.tif", 9, "VALUE", remap_floodzones],
    ["Reclass_Hospitals.tif", 9, "VALUE", remap_hospitals],
    ["Reclass_PoliceCommunity.tif", 9, "VALUE", remap_policeCommunity],
    ["Reclass_Roads.tif", 9, "VALUE", remap_roads],
    ["Reclass_Schools.tif", 9, "VALUE", remap_schools],
    ["Reclass_SewerCon.tif", 9, "VALUE", remap_sewerCon],
    ["Reclass_Slope.tif", 9, "VALUE", remap_slope],
    ["Reclass_Wetlands.tif", 9, "VALUE", remap_wetlands],
    ["landuse.tif", 10 , "VALUE", remap_landuse]
], [1, 10, 1])


# Execute WeightedOverlay
outWeightedOverlay = WeightedOverlay(myWOTable)

# Save the output
outWeightedOverlay.save(r"C:\Users\Dominic\Desktop\ParsuitAPX\ParSuit\WeightedOverlay_PyTest.tif")

# Print a message confirming the script has run
print("Script completed successfully")

