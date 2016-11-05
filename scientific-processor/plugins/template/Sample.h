#ifndef __SAMPLE_CLASS_H__
#define __SAMPLE_CLASS_H__





class Sample
{
private:
  std::string concatString(const char *  s1, const char * s2);
  void processRasterData(float * rasterData, int nXSize, int nYSize, float * dest);
  void manageRasterIO(GDALRasterBand * band, int nXSize, int nYSize, GDALRWFlag flag, float * rasterMatrix);
public:
  Sample();
  const char * PROCESSED_IMAGE_FILENAME ;
  void process(char *  productPath, char * destinationPath);
  void translationJP2_GTIFF(char * productPath, char * destinationPath);
};

#endif