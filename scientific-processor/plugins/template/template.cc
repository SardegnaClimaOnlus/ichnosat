
#include <string>
#include <stdlib.h>
#include <iostream>
#include "gdal.h"
#include "gdal_alg.h"
#include "gdal_priv.h"
#include "Sample.h"

extern "C" char * process(char * productPath, char * destinationPath)
{
  Sample * sample = new Sample();
  std::string result = sample->process(productPath, destinationPath);
  delete sample;

  return productPath;

}