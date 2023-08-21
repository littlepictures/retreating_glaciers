#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import numpy as np
# from scipy import ndimage
from scipy import signal
from osgeo import gdal
from osgeo.gdalconst import *


gdal.DontUseExceptions()

#Setup variables

# Parse command line arguments.
i = 1
while i < len(sys.argv):
 arg = sys.argv[i]

 if arg == "-o":
  i = i + 1
  out_file = sys.argv[i]

 elif arg == "-i":
  i = i + 1
  in_file = sys.argv[i]

 elif arg == "-filt" :
  i = i + 1
  filtersize = int(sys.argv[i])
 i = i + 1

INPUT_DATA=in_file
OFILE=out_file

#Read in with gdal
inDs = gdal.Open(INPUT_DATA)

#Get data and geotransform info
geotransform = inDs.GetGeoTransform()
rows = inDs.RasterYSize
cols = inDs.RasterXSize
array2process_r = np.array(inDs.GetRasterBand(1).ReadAsArray())
array2process_g = np.array(inDs.GetRasterBand(2).ReadAsArray())
array2process_b = np.array(inDs.GetRasterBand(3).ReadAsArray())

#Sort array in case of NAN values
workarr_r = np.nan_to_num(array2process_r)
workarr_g = np.nan_to_num(array2process_g)
workarr_b = np.nan_to_num(array2process_b)

#Apply function across dataset
processedArray_r=signal.medfilt2d(workarr_r, kernel_size=filtersize)
processedArray_g=signal.medfilt2d(workarr_g, kernel_size=filtersize)
processedArray_b=signal.medfilt2d(workarr_b, kernel_size=filtersize)



#~~~~~~~~~~~~~~~~~
#Write out dataset, assigning geotransform info of the input dataset
# - assumes that output array has the same dimensions as the input arrayl

#Create the output gdal object
driver = inDs.GetDriver()


outDs = driver.Create(OFILE, cols, rows, 3, gdal.GDT_Byte)
if outDs is None:
    sys.exit("Unable to create %s" %OFILE)


outBand_r = outDs.GetRasterBand(1)
outBand_g = outDs.GetRasterBand(2)
outBand_b = outDs.GetRasterBand(3)


# write the data
outBand_r.WriteArray(processedArray_r)
outBand_g.WriteArray(processedArray_g)
outBand_b.WriteArray(processedArray_b)

# georeference the data and set the projection based on input dataset
outDs.SetGeoTransform(inDs.GetGeoTransform())
outDs.SetProjection(inDs.GetProjection())
outBand_r.SetNoDataValue(np.nan)
outBand_g.SetNoDataValue(np.nan)
outBand_b.SetNoDataValue(np.nan)

outBand_r.FlushCache()
outBand_g.FlushCache()
outBand_b.FlushCache()
