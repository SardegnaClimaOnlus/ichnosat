#include <stdio.h>
#include <iostream>
#include <string>
#include <stdlib.h>
#include "cpl_port.h"
#include "gdal.h"
#include "gdal_alg.h"
#include "gdal_priv.h"
#include "gdal_utils.h"
#include "cpl_conv.h"
#include "ogr_srs_api.h"
#include "cpl_string.h"
#include "cpl_conv.h"
#include "cpl_multiproc.h"
#include "gdal_frmts.h"
#include "ogrsf_frmts.h"
#include "ogr_core.h"
#include "Sample.h"


std::string Sample::ConcatString(const char * s1, const char * s2){
     std::string a(s1);
     std::string b(s2);
     std::string concat = a + b;
  return concat.c_str();
}

void Sample::ProcessRasterData(float * band4_raster, float * band8_raster, int nXSize, int nYSize, float * ndvi_raster){
  // Reflectance 
  for(int i=0; i< nXSize*nYSize; i++){
    band4_raster[i]=(float)band4_raster[i] / (float)10000;
    band8_raster[i]=(float)band8_raster[i] / (float)10000;
  }
  // NDVI
  for(int i=0; i< nXSize*nYSize; i++){
    ndvi_raster[i] = (band8_raster[i] - band4_raster[i])/(band8_raster[i] + band4_raster[i]);

  }
  std::cout << "debug => check- band4_raster[100000]: " << band4_raster[100000]<<" , ndvi_raster[100000]: " << ndvi_raster[100000] << std::endl;
}


void Sample::process(char * productPath, char * ndvi_rasterinationPath){

  const char * DEST_FORMAT = "GTiff";
  const char * BAND4_FILENAME = "B04.jp2";
  const char * BAND8_FILENAME = "B08.jp2";
  const char * PROCESSED_IMAGE_FILENAME = "NVDI.tif";
  GDALDriver * poDriver;

  // load drivers
  GDALAllRegister();

  // load driver for geotiff
  poDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);

  // calculate source and ndvi_rasterination paths
  std::string band4_path = this->ConcatString(productPath, BAND4_FILENAME);
  std::string band8_path = this->ConcatString(productPath, BAND8_FILENAME);
  std::string ndvi_rasterinationAbsolutePath = this->ConcatString(ndvi_rasterinationPath, PROCESSED_IMAGE_FILENAME);
  std::cout << "band4_path" << band4_path << std::endl;
  std::cout << "band8_path" << band8_path << std::endl;
  std::cout << "ndvi_rasterination path " << ndvi_rasterinationAbsolutePath << std::endl;



  // open band4 file
  GDALDataset * band4_dataset = (GDALDataset *) GDALOpen( band4_path.c_str(), GA_ReadOnly );
  GDALDataset * band8_dataset = (GDALDataset *) GDALOpen( band8_path.c_str(), GA_ReadOnly );

  // get band B04
  GDALRasterBand  *band4_band01;
  band4_band01 = band4_dataset->GetRasterBand( 1 );
  
  // get band B08
  GDALRasterBand  * band8_band01;
  band8_band01 = band8_dataset->GetRasterBand( 1 );

  // get raster data
  float * band4_raster;
  float * band8_raster;
  float * ndvi_raster;
  int   nXSize = band4_band01->GetXSize();
  int   nYSize = band4_band01->GetYSize();

  //////// BEGIN CREATE PROCESSED FILE ///////
  // create new file
  GDALDataset * nvdi_dataset = poDriver->Create( ndvi_rasterinationAbsolutePath.c_str(), nXSize, nYSize, 1, GDT_Float32,NULL );

  // copy geo tranformation
  double adfGeoTransform[6];
  band4_dataset->GetGeoTransform(adfGeoTransform);
  nvdi_dataset->SetGeoTransform( adfGeoTransform );

  // copy projection
  const char * pszProjection;
  pszProjection = band4_dataset->GetProjectionRef();
  nvdi_dataset->SetProjection(pszProjection);

  //////// END CREATE PROCESSED FILE ///////

  // allocate memory
  band4_raster = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);
  band8_raster = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);
  ndvi_raster = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);

  // read raster data
  CPLErr err = band4_band01->RasterIO(GF_Read,0,0,nXSize,nYSize,band4_raster,nXSize,nYSize,GDT_Float32,0,0);
  std::cout << err << std::endl;

  err = band8_band01->RasterIO(GF_Read,0,0,nXSize,nYSize,band8_raster,nXSize,nYSize,GDT_Float32,0,0);
  std::cout << err << std::endl;

  // process raster data
  this->ProcessRasterData(band4_raster,band8_raster,nXSize,nYSize,ndvi_raster);

  // write data
  err = nvdi_dataset->RasterIO(GF_Write,0,0,nXSize,nYSize,ndvi_raster,nXSize,nYSize,GDT_Float32,1,NULL,0,0,0,NULL);
  std::cout << err << std::endl;

  // close file
  if( nvdi_dataset != NULL )
    GDALClose( (GDALDatasetH) nvdi_dataset );
  if( band4_dataset != NULL )
    GDALClose( (GDALDatasetH) band4_dataset );
   if( band8_dataset != NULL )
    GDALClose( (GDALDatasetH) band8_dataset );

  // free allocated memory
  CPLFree( band4_raster );
  CPLFree( band8_raster )
  CPLFree( ndvi_raster );

  return ;
}
