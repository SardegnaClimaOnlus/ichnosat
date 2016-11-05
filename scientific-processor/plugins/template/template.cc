
#include <string>
#include <stdlib.h>
#include <iostream>
#include "gdal.h"
#include "gdal_alg.h"
#include "gdal_priv.h"
#include "Sample.h"

extern "C" void process(char * productPath, char * destinationPath)
{
  Sample * sample = new Sample();
   sample->process(productPath, destinationPath);
  delete sample;

  return ;

}