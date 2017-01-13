# Build plugin

```
g++ -fPIC -shared -I/usr/local/include /usr/lib/libgdal.so.20.1.1  *.cc -o build/template.so
```

# Run load_test

process

- load gdal drivers
- create geotiff driver

- generate source and destination file paths
- open B04 file
- open B08 file
- extract band of B04 file
- extract band of B08 file
- extract image size from B04 file

- create destination dataset (nvdi_dataset)
- copy geo transformation from B04 to nvdi
- copy projection data from B04 to nvdi
- process raster data:
    - extract a row from B04 and B08
    - get reflectance and Radiance from rows
    - calculate ndvi row
    - store ndvi row in the ndvi buffer
- write ndvi buffer in destination file
- close files
- free memory