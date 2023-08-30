# little picture - glacier retreat 

## Background on this CLIP
As the climate warms, glaciers around the world are losing ice. In Europe, the extent of glaciers has been charted on topographic maps since the nineteenth century and by air survey since the middle of the twentieth century. Satellites have been able to monitor glaciers worldwide since the launch of Landsat in 1973. This picture shows a 12 kilometre-wide area around Zermatt in Switzerland, including the Gorner and Findel Glaciers, which have retreated about 3 km since 1850. The area covered by ice is shown for 1850, 1931, 1973, and 2010 based on historical maps and air photos, and for 2015 based on Copernicus Sentinel-2 satellite images.

## Data Sources
The CLIP uses the following datasets:
- Glacier Monitoring in Switzerland (GLAMOS) database. https://glamos.ch/en/downloads#inventories/A55f-03
- ESA-CCI Glaciers team. https://doi.pangaea.de/10.1594/PANGAEA.909133

## Data Preparation & Creating Visualizations
Uses included Python script "gdal_median.py", which requires the scipy library as well as gdal to be installed.
Command line instructions should operate under any environment with Python and GDAL installed (including OSGeo4W, Cygwin, etc)

1830
Clip swiss glacier inventory to area of interest (around Zermatt)
```
ogr2ogr -f GeoJSON SGI_1850.json inventory_sgi1850_r1992/SGI_1850.shp
ogr2ogr -f GeoJSON -clipsrc 2621250 1087000 2633400 1099150 glacier_1850_area.jsn inventory_sgi1850_r1992/SGI_1850.shp
```
1931
Swiss glacier inventory uses old grid for 1931 only, reproject to new grid first
```
ogr2ogr -f GeoJSON -t_srs "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +units=m +no_defs +wktext" 1931_complete.jsn inventory_sgi1931_r2022/SGI_1931.shp
```

### Clip to area
```
ogr2ogr -f GeoJSON -clipsrc 2621250 1087000 2633400 1099150 glacier_1931_area.jsn 1931_complete.jsn
```
1973
```
ogr2ogr -f GeoJSON -clipsrc 2621250 1087000 2633400 1099150 glacier_1973_area.jsn  inventory_sgi1973_r1976/SGI_1973.shp
```
2010
```
ogr2ogr -f GeoJSON  -clipsrc 2621250 1087000 2633400 1099150 glacier_2010_area.jsn inventory_sgi2010_r2010/SGI_2010.shp
```
2016
```
ogr2ogr -f GeoJSON   -clipsrc 2621250 1087000 2633400 1099150 glacier_2016_area.jsn inventory_sgi2016_r2020/SGI_2016_glaciers.shp
```

### create initial image (extents and size shown) with earliest data, against a brown background using dark blue
```
gdal_rasterize -init 118 72 22 -ot Byte -burn 37 -burn 122 -burn 203 -te 2621250 1087000 2633400 1098500 -ts 3240 3240 glacier_1850_area.jsn 1850_glaciers.tif
```
### Median filter (using script included here) 11 pixel kernel to smooth outlines. The filter kernel size must be an odd number
```
python gdal_median.py -i 1850_glaciers.tif -o 1850_glaciers_median.tif -filt 11
```
### Rasterize 1931 data using (26, 174, 202) colours, into black background with black as nodata
```
gdal_rasterize -ot Byte -burn 26 -burn 174 -burn 202 -a_nodata 0 -te 2621250 1087000 2633400 1098500 -ts 3240 3240 glacier_1931_area.jsn 1931_glaciers.tif
python gdal_median.py -i 1931_glaciers.tif -o 1931_glaciers_median.tif -filt 11
```
### Rasterize 1973 data using (88,225,203) colours, into black background with black as nodata
```
gdal_rasterize -ot Byte -burn 88 -burn 225 -burn 203 -a_nodata 0 -te 2621250 1087000 2633400 1098500 -ts 3240 3240 glacier_1973_area.jsn 1973_glaciers.tif
python gdal_median.py -i 1973_glaciers.tif -o 1973_glaciers_median.tif -filt 11
```
### Rasterize 2010 data using (148, 255, 244) colours, into black background with black as nodata
```
gdal_rasterize -ot Byte -burn 148 -burn 255 -burn 244 -a_nodata 0 -te 2621250 1087000 2633400 1098500 -ts 3240 3240 glacier_2010_area.jsn 2010_glaciers.tif
python gdal_median.py -i 2010_glaciers.tif -o 2010_glaciers_median.tif -filt 11
```
### Rasterize 2016 data using (255, 255, 255) colours, into black background with black as nodata
```
gdal_rasterize -ot Byte -burn 255 -burn 255 -burn 255 -a_nodata 0 -te 2621250 1087000 2633400 1098500 -ts 3240 3240 glacier_2016_area.jsn 2016_glaciers.tif
python gdal_median.py -i 2016_glaciers.tif -o 2016_glaciers_median.tif -filt 11
```
### Combine all coloured images using black/0 as no data value
```
gdal_merge -co COMPRESS=LZW -o glaciers_map.tif -n 0 1850_glaciers_median.tif 1931_glaciers_median.tif 1973_glaciers_median.tif 2010_glaciers_median.tif 2016_glaciers_median.tif
```

## CREDITS & LICENSE
- Idea by: [Planetary Visions Limited]([https://climate.esa.int/](http://www.planetaryvisions.com/index.php))
- Processing Scripts by: [Planetary Visions Limited]([https://climate.esa.int/](http://www.planetaryvisions.com/index.php))
- Visualization by: [Planetary Visions Limited]([https://climate.esa.int/](http://www.planetaryvisions.com/index.php))

The code in this repository is published under [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/)
