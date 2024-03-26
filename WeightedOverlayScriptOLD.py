# Name: WeightedOverlayScript.py
# Description: Overlays several rasters using a common scale and weighing
#              each according to its importance.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import shutil

# Set environment settings
arcpy.env.cellSize = 150
arcpy.env.scratchWorkspace = r"C:\Users\Dominic\Desktop\ParSuitAPRX"
arcpy.env.overwriteOutput = True

# Set local variables
inRaster1 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Brownfield.tif"
inRaster2 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_BuildableSoil.tif"
inRaster3 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Floodzones.tif"
inRaster4 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Hospitals.tif"
inRaster5 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_PoliceCommunity.tif"
inRaster6 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Roads.tif"
inRaster7 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Schools.tif"
inRaster8 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_SewerCon.tif"
inRaster9 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Slope.tif"
inRaster10 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\Reclass_Wetlands.tif"
inRaster11 = r"C:\Users\Dominic\Desktop\ParSuitAPRX\landuse.gdb\landuse"

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
with open("slider_values.txt", "r") as file:
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
outWeightedOverlay.save(r"C:\Users\Dominic\Desktop\ParSuitAPRX\output.tif")

print("Weighted Overlay completed successfully!")

#Convert output raster to polygon
arcpy.RasterToPolygon_conversion(outWeightedOverlay, r"C:\Users\Dominic\Desktop\ParSuitAPRX\raster_polygon.shp", "NO_SIMPLIFY", "VALUE")
print("Raster to Polygon completed successfully!")

#Dissolve output polygon based on the gridcode field
arcpy.Dissolve_management(r"C:\Users\Dominic\Desktop\ParSuitAPRX\raster_polygon.shp", r"C:\Users\Dominic\Desktop\ParSuitAPRX\dissolved_polygon.shp", "gridcode", "", "MULTI_PART")
print("Dissolve completed successfully!")

#Convert disolved polygon to geojson
arcpy.FeaturesToJSON_conversion(r"C:\Users\Dominic\Desktop\ParSuitAPRX\dissolved_polygon.shp", r"C:\Users\Dominic\Desktop\ParSuitAPRX\WeightedOverlay.geojson", "FORMATTED", "NO_Z_VALUES", "NO_M_VALUES", "GEOJSON", "WGS84", "USE_FIELD_NAME")
print("Conversion to GeoJSON completed successfully!")

# Move the geojson file to the ParSuit Data folder and rename it to RasterOverlay.geojson
shutil.move(r"C:\Users\Dominic\Desktop\ParSuitAPRX\WeightedOverlay.geojson", r"C:\Users\Dominic\Desktop\ParSuit\data\RasterOverlay.geojson", copy_function=shutil.copy2)
print("GeoJSON file moved successfully!")
