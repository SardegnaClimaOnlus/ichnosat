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
    std::cout << rasterMatrix[i] << "->" << dest[i] << std::endl;
  }


}

void Sample::manageRasterIO(GDALRasterBand * band, int nXSize, int nYSize, GDALRWFlag flag, float * rasterMatrix){
  CPLErr err = band->RasterIO( flag, 	    //GDALRWFlag  	eRWFlag
			      0,       	    // int  	    nXOff
			      0,       	    // int  	    nYOff
			      nXSize,  	    //int  	        nXSize
			      nYSize,       //int  	        nYSize
                  rasterMatrix, //void      *  	pData
			      nXSize, 	    //int  	        nBufXSize
			      nYSize, 	    //int  	        nBufYSize
			      GDT_Float32,  //GDALDataType  eBufType
                  0, 		    //GSpacing  	nPixelSpace
			      0);           //GSpacing  	nLineSpace
  std::cout << err << std::endl;
}

void rasterIO(GDALDataset * dataset, int nXSize, int nYSize, GDALRWFlag flag, float * rasterMatrix){


 dataset->RasterIO 	( 	flag,
		0, //int  	nXOff,
		0, //int  	nYOff,
		nXSize, ///int  	nXSize,
		nYSize, //int  	nYSize,
		rasterMatrix,//void *  	pData,
		nXSize, //int  	nBufXSize,
		nYSize, //int  	nBufYSize,
		GDT_Float32, //GDALDataType  	eBufType,
		1, //int  	nBandCount,
		NULL, //int *  	panBandMap,
		0, //GSpacing  	nPixelSpace,
		0, //GSpacing  	nLineSpace,
		0, //GSpacing  	nBandSpace,
		NULL //GDALRasterIOExtraArg *  	psExtraArg
	);
	}


void Sample::process(char * productPath, char * destinationPath){

  const char * DEST_FORMAT = "GTiff";
  const char * PROCESSED_IMAGE_FILENAME = "processedsmall.tif";
  const char * TMP_IMAGE_FILENAME = "small.tif";
  GDALDriver * poDriver;

  //char **  	srcMetadata;



  // load drivers
  GDALAllRegister();

  // load driver for geotiff
  poDriver = GetGDALDriverManager()->GetDriverByName(DEST_FORMAT);


  std::string absolutePath = this->concatString(productPath, TMP_IMAGE_FILENAME);
  std::string destinationAbsolutePath = this->concatString(destinationPath, PROCESSED_IMAGE_FILENAME);

  // open origin file
  GDALDataset *poSrcDS = (GDALDataset *) GDALOpen( absolutePath.c_str(), GA_Update );
  std::cout << "tmp source" << absolutePath << std::endl;
  std::cout << "destination path " << destinationAbsolutePath << std::endl;
  GDALDataset *poDstDS;
  //srcMetadata = poSrcDS->GetMetadata();


  // ---- //
//  char **papszOptions = NULL;
//  papszOptions = CSLSetNameValue( papszOptions, "ot", "Float32" );

  // ---- //

  // create a copy
  //poDstDS = poDriver->CreateCopy( destinationAbsolutePath.c_str(), poSrcDS, FALSE,papszOptions, NULL, NULL  );

  // get band
  GDALRasterBand  *poBand;
  poBand = poSrcDS->GetRasterBand( 1 );

  // get raster data
  float * rasterMatrix;
  float * dest;
  int   nXSize = poBand->GetXSize();
  int   nYSize = poBand->GetYSize();


   // new file
  poDstDS = poDriver->Create( destinationAbsolutePath.c_str(), nXSize, nYSize, 1, GDT_Float32,NULL );
  //------//
  //double adfGeoTransform[6] = { 444720, 30, 0, 3751320, 0, -30 };
  double adfGeoTransform[6];
  //OGRSpatialReference oSRS;
  //char *pszSRS_WKT = NULL;
  //GDALRasterBand *poBand;
  poSrcDS->GetGeoTransform(adfGeoTransform);
  poDstDS->SetGeoTransform( adfGeoTransform );
  //oSRS.SetUTM( 11, TRUE );
  //oSRS.SetWellKnownGeogCS( "NAD27" );
  //oSRS.exportToWkt( &pszSRS_WKT );

  const char *  	pszProjection;



  //SetProjection 	( 	const char *  	pszProjection	);
  pszProjection = poSrcDS->GetProjectionRef();
  poDstDS->SetProjection(pszProjection);
  //  CPLFree( pszSRS_WKT );
  //poBand = poDstDS->GetRasterBand(1);
  //poBand->RasterIO( GF_Write, 0, 0, 512, 512,abyRaster, 512, 512, GDT_Byte, 0, 0 );
  /* Once we're done, close properly the dataset */
  //GDALClose( (GDALDatasetH) poDstDS );


  //-----//

  //poDstDS->SetMetadata(srcMetadata,NULL);

  std::cout << "nXSize: " << nXSize << ", nYSize: " << nYSize << std::endl;
  rasterMatrix = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);
  dest = (float *) CPLMalloc(sizeof(float)*nXSize * sizeof(float)*nYSize);

  //rasterIO(poSrcDS, nXSize, nYSize, GF_Read, rasterMatrix);

  // read raster data
  this->manageRasterIO(poBand, nXSize, nYSize,  GF_Read, rasterMatrix);

  // process raster data
  this->processRasterData(rasterMatrix,nXSize,nYSize,dest);

  rasterIO(poDstDS, nXSize, nYSize, GF_Write, dest);

  // write raster data
  //this->manageRasterIO(poBand, nXSize, nYSize,  GF_Write, dest);

  // close file
  if( poDstDS != NULL )
    GDALClose( (GDALDatasetH) poDstDS );
  if( poSrcDS != NULL )
    GDALClose( (GDALDatasetH) poSrcDS );

  CPLFree( rasterMatrix );
  CPLFree( dest );

  return ;
}
