#ifndef __SAMPLE_CLASS_H__
#define __SAMPLE_CLASS_H__

class Sample{
 private:
  std::string ConcatString(const char *  s1, const char * s2);
  void ProcessRasterData(GDALRasterBand * band4_buffer, GDALRasterBand * band8_buffer, int nXSize, int nYSize, float * ndvi_raster);

 public:
  void process(char *  productPath, char * destinationPath);

};

#endif