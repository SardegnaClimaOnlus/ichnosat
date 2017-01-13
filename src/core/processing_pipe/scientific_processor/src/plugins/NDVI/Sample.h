#ifndef __SAMPLE_CLASS_H__
#define __SAMPLE_CLASS_H__

class Sample{
 private:
  std::string ConcatString(const char *  s1, const char * s2);
  void ProcessRasterData(GDALRasterBand * band4_buffer, GDALRasterBand * band8_buffer, int nXSize, int nYSize, float * ndvi_raster);
  GDALDriver * gtiffDriver;
  const char * test(const char * first, const char * second);

 public:
  Sample();
  void process(char *  productPath, char * destinationPath);

};

#endif