#ifndef __SAMPLE_CLASS_H__
#define __SAMPLE_CLASS_H__

class Sample
{
private:
    std::string concatString(const char *  s1, const char * s2);

public:
  Sample();

  int sum(int a, int b);
  char * process(char *  productPath, char * destinationPath);
};

#endif