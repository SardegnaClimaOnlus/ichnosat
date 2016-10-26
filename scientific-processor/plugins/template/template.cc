
#include <string>
#include <stdlib.h>
#include <iostream>
#include "Sample.h"

extern "C" char * process(char * productPath, char * destinationPath)
{
  Sample * sample = new Sample();
  std::string result = sample->process(productPath, destinationPath);
  delete sample;

  return productPath;

}