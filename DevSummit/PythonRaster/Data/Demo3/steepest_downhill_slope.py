import math
import arcpy
from arcpy.sa import Raster, RasterCellIterator

arcpy.env.overwriteOutput = True

print('Read input DEM...')
dem = Raster(r'C:\DevSummit\PythonRaster\Data\Demo3\Input\dem')
cell_x, cell_y = dem.getRasterInfo().getCellSize()
raster_info = dem.getRasterInfo()

# Set the output pixel type to be float 32
raster_info.setPixelType('F32')
min_slope = Raster(raster_info)
print('Start calculating minimum slope...')
with RasterCellIterator({'rasters':[dem, min_slope]}) as rci:
    for r,c in rci:
        slopes = []
        # Iterate through 8 neighbors
        for x,y in [(-1,-1),(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,1),(1,-1)]:
            # Calculate the slope from center cell to each neighbor
            slope = abs(dem[r,c]-dem[r+x,c+y])/math.sqrt(cell_x**2+cell_y**2)
            # Add all the slope values to a list
            slopes.append(slope)
        # Assign the minimum slope to the output cell value
        min_slope[r,c] = min(slopes)
print('Calculation finished.')
min_slope.save(r'C:\DevSummit\PythonRaster\Data\Demo3\Output\new_slope')
print('Output has been saved.')
