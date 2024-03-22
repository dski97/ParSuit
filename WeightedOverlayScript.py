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
    [inRaster11, 10, "VALUE", remapLanduse]
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