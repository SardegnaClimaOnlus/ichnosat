//    ====================================================================================
//     __     ______     __  __     __   __     ______     ______     ______     ______
//    /\ \   /\  ___\   /\ \_\ \   /\ "-.\ \   /\  __ \   /\  ___\   /\  __ \   /\__  _\
//    \ \ \  \ \ \____  \ \  __ \  \ \ \-.  \  \ \ \/\ \  \ \___  \  \ \  __ \  \/_/\ \/
//     \ \_\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\  \ \_\ \_\    \ \_\
//      \/_/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/   \/_/\/_/     \/_/
//
//    ====================================================================================
//
//    Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
//
//    Permission is hereby granted, free of charge, to any person obtaining a copy of
//    this software and associated documentation files (the "Software"), to deal in
//    the Software without restriction, including without limitation the rights to
//    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
//    of the Software, and to permit persons to whom the Software is furnished to do
//    so, subject to the following conditions:
//
//    The above copyright notice and this permission notice shall be included in all
//    copies or substantial portions of the Software.
//
//    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//    SOFTWARE.
//
//    ====================================================================================

#include <stdio.h>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <limits>
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
#include "NDVI.h"

char * NDVI::ConcatString(const char * first, const char * second){
  size_t first_len = first?strlen(first):0;
  size_t second_len = second?strlen(second):0;
  char * concat = (char*) CPLMalloc((first_len+1+second_len+1) * sizeof(char));
  concat = strcpy(concat, first);
  concat = strcat(concat, second);
  return concat;
}

void NDVI::ProcessRasterData(GDALRasterBand * band4_band01, GDALRasterBand * band8_band01, int nXSize, int nYSize, float * ndvi_raster){
  float * band4_buffer = (float *) CPLMalloc(sizeof(float)*nXSize);
  float * band8_buffer  = (float *) CPLMalloc(sizeof(float)*nXSize);
  CPLErr err;
  for(int i=0; i< nYSize; i++){
    // read raster data
    err = band4_band01->RasterIO(GF_Read,0,i,nXSize,1,band4_buffer,nXSize,1,GDT_Float32,0,0);
    if(err > 0) std::cout << "err: " << err << std::endl;

    err = band8_band01->RasterIO(GF_Read,0,i,nXSize,1,band8_buffer,nXSize,1,GDT_Float32,0,0);
    if(err > 0) std::cout << "err: " << err << std::endl;

    for(int j = 0;j < nXSize; j++){
        band4_buffer[j]=(float)band4_buffer[j] / (float)10000;
        if(band4_buffer[j] > 0.2){
            ndvi_raster[i*nXSize+j] = std::numeric_limits<float>::max();
        }
        else{
            band8_buffer[j]=(float)band8_buffer[j] / (float)10000;
            ndvi_raster[i*nXSize+j] = (band8_buffer[j] - band4_buffer[j])/(band8_buffer[j] + band4_buffer[j]);
        }
    }
  }
  if(band4_buffer != NULL ) CPLFree( band4_buffer );
  if(band8_buffer != NULL ) CPLFree( band8_buffer );

}


void NDVI::process(char * productPath, char * ndvi_rasterinationPath){

  const char * DEST_FORMAT = "GTiff";
  const char * BAND4_FILENAME = "B04.jp2";
  const char * BAND8_FILENAME = "B08.jp2";
  const char * PROCESSED_IMAGE_FILENAME = "NVDI.tif";

  std::cout <<"[scientific-processor][NDVI_plugin]: Start processing" << std::endl;
  GDALDriver * poDriver;

  // load drivers
  GDALAllRegister();

  // load driver for geotiff
  poDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);

  // open band4 file and band8 file
  char * band4_path = this->ConcatString(productPath, BAND4_FILENAME);
  char * band8_path = this->ConcatString(productPath, BAND8_FILENAME);
  GDALDataset * band4_dataset = (GDALDataset *) GDALOpen( ( const char *) band4_path, GA_ReadOnly );
  GDALDataset * band8_dataset = (GDALDataset *) GDALOpen( ( const char *) band8_path, GA_ReadOnly );
  if(band4_path != NULL) CPLFree( (void * ) band4_path);
  if(band8_path != NULL) CPLFree( (void * ) band8_path);


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

  // create new file
  GDALDataset * nvdi_dataset = poDriver->Create( this->ConcatString(ndvi_rasterinationPath, PROCESSED_IMAGE_FILENAME), nXSize, nYSize, 1, GDT_Float32,NULL );

  // copy geo tranformation
  double adfGeoTransform[6];
  band4_dataset->GetGeoTransform(adfGeoTransform);
  nvdi_dataset->SetGeoTransform( adfGeoTransform );

  // copy projection
  const char * pszProjection;
  pszProjection = band4_dataset->GetProjectionRef();
  nvdi_dataset->SetProjection(pszProjection);

  // process raster data
  this->ProcessRasterData(band4_band01, band8_band01, nXSize,nYSize,ndvi_raster);

  // write data
  CPLErr err = nvdi_dataset->RasterIO(GF_Write,0,0,nXSize,nYSize,ndvi_raster,nXSize,nYSize,GDT_Float32,1,NULL,0,0,0,NULL);
  if(err > 0) std::cout << "err: " << err << std::endl;

  // close file
  if( nvdi_dataset != NULL ) GDALClose( (GDALDatasetH) nvdi_dataset );
  if( band4_dataset != NULL ) GDALClose( (GDALDatasetH) band4_dataset );
  if( band8_dataset != NULL ) GDALClose( (GDALDatasetH) band8_dataset );

  // free allocated memory
  if( ndvi_raster != NULL ) CPLFree( ndvi_raster );

  return ;
}