import numpy as np
import arcpy
from arcpy.sa import Raster, RasterCellIterator

arcpy.env.overwriteOutput = True

inDEM = arcpy.GetParameterAsText(0)
outslope = arcpy.GetParameterAsText(1)   

arcpy.AddMessage('Read input DEM...')
dem = Raster(inDEM)
cell_x, cell_y = dem.getRasterInfo().getCellSize()
raster_info = dem.getRasterInfo()

# Set the output pixel type to be float 32
raster_info.setPixelType('F32')
new_slope = Raster(raster_info)

arcpy.AddMessage('Start calculating steepest downhill neighbor slope...')
with RasterCellIterator({'rasters':[dem, new_slope]}) as rci:
    for r,c in rci:
        slopes = []
        
        # Iterate through 8 neighbors
        for x,y in [(-1,-1),(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,1),(1,-1)]:
            # Calculate the slope from center cell to each neighbor
            if dem[r,c] >= dem[r+x,c+y]: # only look for downhill slope
                slope = abs(dem[r,c]-dem[r+x,c+y]) / np.sqrt((x*cell_x)**2+(y*cell_y)**2)
                slopes.append(slope)
        
        # Assign the steepest slope to the output cell value
        if len(slopes) != 0:
            new_slope[r,c] = max(slopes)
        
arcpy.AddMessage('Calculation finished.')
new_slope.save(outslope)
arcpy.AddMessage('Output has been saved.')
