#include <stdio.h>
#include <iostream>
#include <string>
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
#include <iostream>
#include <stdlib.h>
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

char * Sample::process(char * productPath, char * destinationPath){

  const char * DEST_FORMAT = "GTiff";
  const char * FIRST_BAND_FILENAME = "BAND_1.jp2";
  const char * PROCESSED_IMAGE_FILENAME = "BAND_1.tif";


  GDALAllRegister();

  GDALDriver *poDriver;
  char **papszMetadata;
  poDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);
  if( poDriver == NULL ){
    std::cout << "the driver is null" << std::endl;
    exit( 1 );
  }
  papszMetadata = poDriver->GetMetadata();
  if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATE, FALSE ) )
    printf( "Driver %s supports Create() method.\n", DEST_FORMAT );
  if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATECOPY, FALSE ) )
    printf( "Driver %s supports CreateCopy() method.\n", DEST_FORMAT );

  std::string absolutePath = this->concatString(productPath, FIRST_BAND_FILENAME);
  const char * absolutePathC =  absolutePath.c_str();

  std::string destinationAbsolutePath = this->concatString(destinationPath, PROCESSED_IMAGE_FILENAME);
  const char * destinationAbsolutePathC =  destinationAbsolutePath.c_str();

  GDALDataset *poSrcDS = (GDALDataset *) GDALOpen( absolutePathC, GA_ReadOnly );
  GDALDataset *poDstDS;
  poDstDS = poDriver->CreateCopy( destinationAbsolutePathC, poSrcDS, FALSE,NULL, NULL, NULL );
  if( poDstDS != NULL )
    GDALClose( (GDALDatasetH) poDstDS );
  GDALClose( (GDALDatasetH) poSrcDS );

  return productPath;
}
int Sample::sum(int a, int b)
{
  return a + b;
}