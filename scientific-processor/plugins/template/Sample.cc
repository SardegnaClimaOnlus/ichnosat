#include <stdio.h>
#include <iostream>
#include <string>
#include "Sample.h"

Sample::Sample()
{
}

char * Sample::process(char * productPath){
    std::cout << "hellofrom sample process " << std::endl;
    std::cout << productPath << std::endl;
    return productPath;
}
int Sample::sum(int a, int b)
{
  return a + b;
}