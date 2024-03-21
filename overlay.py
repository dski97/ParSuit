# Name: WeightedOverlay_Custom.py
# Description: Overlays several rasters using a common scale and weighing 
#    each according to its importance.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy.sa import *

# Set the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Set environment settings with arcpy.EnvManager for scoped setting management
with arcpy.EnvManager(cellSize=100, scratchWorkspace=r"C:\Users\cwalinskid\Downloads\ParSuit\ParSuit\ParSuit", overwriteOutput=True):
    
    # Define the path and weighting for each input raster
    inRasters = [
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Brownfield.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_BuildableSoil.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Floodzones.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Hospitals.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_PoliceCommunity.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Roads.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Schools.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_SewerCon.tif", 9, "Value", RemapValue([[1,1],[2,1],[3,1],[4,1],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Slope.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        (r"C:\Users\cwalinskid\Desktop\ParSuit\Reclass_Wetlands.tif", 9, "Value", RemapValue([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],["NODATA","NODATA"]])),
        # Add other rasters following the same pattern
        (r"C:\Users\cwalinskid\Desktop\ParSuit\landuse.gdb\landuse", 10, "LANDUSE", RemapValue([["Impervious Surfaces",9],["Developed Open Space",8],["Cultivated Land",8],["Pasture/Hay",8],["Grassland",8],["Mixed Forest",7],["Scrub/Shrub",7],["Palustrine Forested Wetland",3],["Palustrine Scrub/Shrub Wetland",3],["Palustrine Emergent Wetland",3],["Estuarine Emergent Wetland",3],["Unconsolidated Shore",3],["Bare Land",10],["Open Water","Restricted"],["Palustrine Aquatic Bed","Restricted"],["''","NODATA"],["NODATA","NODATA"]]))
    ]

    # Create the WOTable
    myWOTable = WOTable([(path, weight, valueType, remap) for path, weight, valueType, remap in inRasters], [1, 10, 1])

    # Execute WeightedOverlay
    outWeightedOverlay = WeightedOverlay(myWOTable)

    # Save the output to the new specified location
    outWeightedOverlay.save(r"C:\Users\cwalinskid\Desktop\ParSuit\ParSuit.gdb\WeightRecallTest")

print("Weighted overlay analysis and save operation completed.")
