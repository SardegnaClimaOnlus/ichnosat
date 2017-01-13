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

Sample::Sample(){

  const char * DEST_FORMAT = "GTiff";

  // load  all gdal drivers
  GDALAllRegister();
  this->gtiffDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);

}

std::string Sample::ConcatString(const char * s1, const char * s2){
     std::string a(s1);
     std::string b(s2);
     std::string concat = a + b;
  return concat.c_str();
}

void Sample::ProcessRasterData(GDALRasterBand * band4_band01, GDALRasterBand * band8_band01, int nXSize, int nYSize, float * ndvi_raster){

  float * band4_buffer = (float *) CPLMalloc(sizeof(float)*nXSize);
  float * band8_buffer  = (float *) CPLMalloc(sizeof(float)*nXSize);
  CPLErr err;
  // Reflectance
  for(int i=0; i< nYSize; i++){
    // read raster data
    err = band4_band01->RasterIO(GF_Read,0,i,nXSize,1,band4_buffer,nXSize,1,GDT_Float32,0,0);

    if(err > 0)
        std::cout << "err: " << err << std::endl;
    err = band8_band01->RasterIO(GF_Read,0,i,nXSize,1,band8_buffer,nXSize,1,GDT_Float32,0,0);
    if(err > 0)
        std::cout << "err: " << err << std::endl;

    for(int j = 0;j < nXSize; j++){
        band4_buffer[j]=(float)band4_buffer[j] / (float)10000;
        band8_buffer[j]=(float)band8_buffer[j] / (float)10000;
        //NDVI = (R08-R04)/(R08+R04)
        ndvi_raster[i*nXSize+j] = (band8_buffer[j] - band4_buffer[j])/(band8_buffer[j] + band4_buffer[j]);
    }
  }
  CPLFree( band4_buffer );
  CPLFree( band8_buffer );

}

const char * Sample::test(const char * first, const char * second){
  std::string a(first);
  std::string b(second);
  std::string concat = a + b;
  return concat.c_str();
}

void Sample::process(char * productPath, char * ndvi_rasterinationPath){


  const char * BAND4_FILENAME = "B04.jp2";
  const char * BAND8_FILENAME = "B08.jp2";
  const char * PROCESSED_IMAGE_FILENAME = "NVDI.tif";

  std::cout <<"[scientific-processor][NDVI_plugin]: Start processing" << std::endl;


  // calculate source and ndvi_rasterination paths
  //std::string band4_path = this->ConcatString(productPath, BAND4_FILENAME);
  //std::string band8_path = this->ConcatString(productPath, BAND8_FILENAME);
  //std::string ndvi_rasterinationAbsolutePath = this->ConcatString(ndvi_rasterinationPath, PROCESSED_IMAGE_FILENAME);

  // open band4 and band8 file
  GDALDataset * band4_dataset = (GDALDataset *) GDALOpen( this->test(productPath, BAND4_FILENAME),
                                                          GA_ReadOnly );
  GDALDataset * band8_dataset = (GDALDataset *) GDALOpen( this->test(productPath, BAND8_FILENAME),
                                                          GA_ReadOnly );

  // get band B04
  GDALRasterBand  *band4_band01;
  band4_band01 = band4_dataset->GetRasterBand( 1 );
  
  // get band B08
  GDALRasterBand  * band8_band01;
  band8_band01 = band8_dataset->GetRasterBand( 1 );

  // get raster data

  int   nXSize = band4_band01->GetXSize();
  int   nYSize = band4_band01->GetYSize();
  float * ndvi_raster = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize) ;

  //////// BEGIN CREATE PROCESSED FILE ///////
  // create new file
  GDALDataset * nvdi_dataset = this->gtiffDriver->Create( this->test(ndvi_rasterinationPath, PROCESSED_IMAGE_FILENAME),
                                                          nXSize,
                                                          nYSize,
                                                          1,
                                                          GDT_Float32,
                                                          NULL );

  // copy geo tranformation
  double adfGeoTransform[6];
  band4_dataset->GetGeoTransform(adfGeoTransform);
  nvdi_dataset->SetGeoTransform( adfGeoTransform );

  // copy projection
  const char * pszProjection;
  pszProjection = band4_dataset->GetProjectionRef();
  nvdi_dataset->SetProjection(pszProjection);

  //////// END CREATE PROCESSED FILE ///////

  // process raster data
  this->ProcessRasterData(band4_band01, band8_band01, nXSize,nYSize,ndvi_raster);

  // write data
  CPLErr err = nvdi_dataset->RasterIO(GF_Write,0,0,nXSize,nYSize,ndvi_raster,nXSize,nYSize,GDT_Float32,1,NULL,0,0,0,NULL);
  if(err > 0)
    std::cout << err << std::endl;

  // close file
  if( nvdi_dataset != NULL )
    GDALClose( (GDALDatasetH) nvdi_dataset );
  if( band4_dataset != NULL )
    GDALClose( (GDALDatasetH) band4_dataset );
   if( band8_dataset != NULL )
    GDALClose( (GDALDatasetH) band8_dataset );

  // free allocated memory
  CPLFree( ndvi_raster );

  return ;
}
