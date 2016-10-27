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

Sample::Sample()
{
}

std::string Sample::concatString(const char * s1, const char * s2){
     std::string a(s1);
     std::string b(s2);
     std::string concat = a + b;
  return concat.c_str();
}

void Sample::processRasterData(float * rasterMatrix, int nXSize, int nYSize){
  for(int x=0;x<nXSize;x++)
    for(int y=0;y<nYSize;y++)
      rasterMatrix[x * nXSize + y] /= 150 ;
}

void Sample::manageRasterIO(GDALRasterBand * band, int nXSize, int nYSize, GDALRWFlag flag, float * rasterMatrix){
  band->RasterIO( flag, 	    //GDALRWFlag  	eRWFlag
			      0,       	    // int  	nXOff
			      0,       	    // int  	nYOff
			      nXSize,  	    //int  	nXSize
			      nYSize,       //int  	nYSize
                  rasterMatrix, //void *  	pData
			      nXSize, 	    //int  	nBufXSize
			      nYSize, 	    //int  	nBufYSize
			      GDT_Float32,  //GDALDataType  	eBufType
                  0, 		    //GSpacing  	nPixelSpace
			      0);           //GSpacing  	nLineSpace
}

char * Sample::process(char * productPath, char * destinationPath){

  const char * DEST_FORMAT = "GTiff";
  const char * FIRST_BAND_FILENAME = "B06.jp2";
  const char * PROCESSED_IMAGE_FILENAME = "B06.tif";
  GDALDriver *poDriver;
  char **papszMetadata;

  // load drivers
  GDALAllRegister();

  // load driver for geotiff
  poDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);
  if( poDriver == NULL ){
    std::cout << "the driver is null" << std::endl;
    exit( 1 );
  }
  // get metadata
  papszMetadata = poDriver->GetMetadata();

  // todo: manage this exceptions
  if( !CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATE, FALSE ) )
     printf( "Driver %s NOT supports Create() method!!\n", DEST_FORMAT );
  if( !CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATECOPY, FALSE ) )
     printf( "Driver %s NOT supports CreateCopy() method!!\n", DEST_FORMAT );

  std::string absolutePath = this->concatString(productPath, FIRST_BAND_FILENAME);
  std::string destinationAbsolutePath = this->concatString(destinationPath, PROCESSED_IMAGE_FILENAME);

  // open origin file
  GDALDataset *poSrcDS = (GDALDataset *) GDALOpen( absolutePath.c_str(), GA_ReadOnly );
  GDALDataset *poDstDS;

  // create a copy
  poDstDS = poDriver->CreateCopy( destinationAbsolutePath.c_str(), poSrcDS, FALSE,NULL, NULL, NULL );

  // get band
  GDALRasterBand  *poBand;
  poBand = poDstDS->GetRasterBand( 1 );

  // get raster data
  float *rasterMatrix;
  int   nXSize = poBand->GetXSize();
  int   nYSize = poBand->GetYSize();
  rasterMatrix = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);
  this->manageRasterIO(poBand, nXSize, nYSize,  GF_Read, rasterMatrix);

  // process raster data
  this->processRasterData(rasterMatrix,nXSize,nYSize);

  // write raster data
  this->manageRasterIO(poBand, nXSize, nYSize,  GF_Write, rasterMatrix);

  // close file
  if( poDstDS != NULL )
    GDALClose( (GDALDatasetH) poDstDS );
  GDALClose( (GDALDatasetH) poSrcDS );

  return productPath;
}
