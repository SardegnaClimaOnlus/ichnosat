
#include <string>
#include <stdlib.h>
#include <iostream>
#include "Sample.h"

extern "C" char * process(char * productPath)
{
  std::cout <<  productPath  << std::endl;
  Sample * sample = new Sample();
  std::string result = sample->process(productPath);
  delete sample;

  return productPath;

}