#include "Sample.h"

extern "C" int sum(int a, int b)
{
  Sample * sample = new Sample();
  int result = sample->sum(a,b);
  delete sample;
  return result;

}