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

void Sample::processRasterData(float * rasterMatrix, int nXSize, int nYSize, float * dest){
  for(int i=0; i< nXSize*nYSize; i++){
    dest[i]=(float)rasterMatrix[i] / (float)10000;
  }
}


void Sample::process(char * productPath, char * destinationPath){



  const char * DEST_FORMAT = "GTiff";
  const char * PROCESSED_IMAGE_FILENAME = "pB06.tif";
  const char * TMP_IMAGE_FILENAME = "B06.tif";
  GDALDriver * poDriver;


  // load drivers
  GDALAllRegister();

  // load driver for geotiff
  poDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);

  // calculate source and destination paths
  std::string absolutePath = this->concatString(productPath, TMP_IMAGE_FILENAME);
  std::string destinationAbsolutePath = this->concatString(destinationPath, PROCESSED_IMAGE_FILENAME);
  std::cout << "tmp source" << absolutePath << std::endl;
  std::cout << "destination path " << destinationAbsolutePath << std::endl;



  // open origin file
  GDALDataset *poSrcDS = (GDALDataset *) GDALOpen( absolutePath.c_str(), GA_Update );

  GDALDataset *poDstDS;

  // get band
  GDALRasterBand  *poBand;
  poBand = poSrcDS->GetRasterBand( 1 );

  // get raster data
  float * rasterMatrix;
  float * dest;
  int   nXSize = poBand->GetXSize();
  int   nYSize = poBand->GetYSize();

  // create new file
  poDstDS = poDriver->Create( destinationAbsolutePath.c_str(), nXSize, nYSize, 1, GDT_Float32,NULL );

  // copy geo tranformation
  double adfGeoTransform[6];
  poSrcDS->GetGeoTransform(adfGeoTransform);
  poDstDS->SetGeoTransform( adfGeoTransform );

  // copy projection
  const char * pszProjection;
  pszProjection = poSrcDS->GetProjectionRef();
  poDstDS->SetProjection(pszProjection);


  // allocate memory
  rasterMatrix = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);
  dest = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);

  // read raster data
  //this->manageRasterIO(poBand, nXSize, nYSize,  GF_Read, rasterMatrix);
  CPLErr err = poBand->RasterIO(GF_Read,0,0,nXSize,nYSize,rasterMatrix,nXSize,nYSize,GDT_Float32,0,0);
  std::cout << err << std::endl;

  // process raster data
  this->processRasterData(rasterMatrix,nXSize,nYSize,dest);

  // write data
  //this->manageRasterIO(poDstDS, nXSize, nYSize, GF_Write, dest);
  poDstDS->RasterIO(GF_Write,0,0,nXSize,nYSize,rasterMatrix,nXSize,nYSize,GDT_Float32,1,NULL,0,0,0,NULL);
  //rasterIO(poDstDS, nXSize, nYSize, GF_Write, dest);

  // close file
  if( poDstDS != NULL )
    GDALClose( (GDALDatasetH) poDstDS );
  if( poSrcDS != NULL )
    GDALClose( (GDALDatasetH) poSrcDS );

  // free allocated memory
  CPLFree( rasterMatrix );
  CPLFree( dest );

  return ;
}
