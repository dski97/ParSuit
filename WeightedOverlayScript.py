# Name: WeightedOverlay_Custom.py
# Description: Overlays several rasters using a common scale and weighing
#              each according to its importance.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
arcpy.env.cellSize = 100
arcpy.env.scratchWorkspace = r"C:\Users\cwalinskid\Desktop\ParSuit"
arcpy.env.overwriteOutput = True

# Set local variables
inRaster1 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Brownfield.tif"
inRaster2 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_BuildableSoil.tif"
inRaster3 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Floodzones.tif"
inRaster4 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Hospitals.tif"
inRaster5 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_PoliceCommunity.tif"
inRaster6 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Roads.tif"
inRaster7 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Schools.tif"
inRaster8 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_SewerCon.tif"
inRaster9 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Slope.tif"
inRaster10 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\Reclass_Wetlands.tif"
inRaster11 = r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\landuse.gdb\\landuse"

remapBrownfield = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapBuildableSoil = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapFloodzones = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapHospitals = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapPoliceCommunity = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapRoads = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapSchools = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapSewerCon = RemapValue([[1,1],[2,1],[3,1],[4,1],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapSlope = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapWetlands = RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])
remapLanduse = RemapValue([["Impervious Surfaces",9],["Developed Open Space",8],["Cultivated Land",8],["Pasture/Hay",8],["Grassland",8],["Mixed Forest",7],["Scrub/Shrub",7],["Palustrine Forested Wetland",3],["Palustrine Scrub/Shrub Wetland",3],["Palustrine Emergent Wetland",3],["Estuarine Emergent Wetland",3],["Unconsolidated Shore",3],["Bare Land",10],["Open Water","Restricted"],["Palustrine Aquatic Bed","Restricted"],["''","NODATA"],["NODATA","NODATA"]])

myWOTable = WOTable([
    [inRaster1, 9, "VALUE", remapBrownfield],
    [inRaster2, 9, "VALUE", remapBuildableSoil],
    [inRaster3, 9, "VALUE", remapFloodzones],
    [inRaster4, 9, "VALUE", remapHospitals],
    [inRaster5, 9, "VALUE", remapPoliceCommunity],
    [inRaster6, 9, "VALUE", remapRoads],
    [inRaster7, 9, "VALUE", remapSchools],
    [inRaster8, 9, "VALUE", remapSewerCon],
    [inRaster9, 9, "VALUE", remapSlope],
    [inRaster10, 9, "VALUE", remapWetlands],
    [inRaster11, 10, "LANDUSE", remapLanduse]
], [1, 10, 1])

# Execute WeightedOverlay
outWeightedOverlay = WeightedOverlay(myWOTable)

# Save the output
outWeightedOverlay.save(r"C:\\Users\\cwalinskid\\Desktop\\ParSuit\\output.tif")

print("Weighted Overlay completed successfully!")