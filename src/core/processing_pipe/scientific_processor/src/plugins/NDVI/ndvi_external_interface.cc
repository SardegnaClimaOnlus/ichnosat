
#include <string>
#include <stdlib.h>
#include <iostream>
#include "gdal.h"
#include "gdal_alg.h"
#include "gdal_priv.h"
#include "NDVI.h"

extern "C" void process(char * productPath, char * destinationPath)
{
  NDVI * ndvi = new NDVI();
   ndvi->process(productPath, destinationPath);
  delete ndvi;

  return ;

}