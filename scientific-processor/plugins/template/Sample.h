#ifndef __SAMPLE_CLASS_H__
#define __SAMPLE_CLASS_H__


#define TMP_IMAGE_FILENAME "figa.tif"


class Sample
{
private:
  std::string concatString(const char *  s1, const char * s2);
  void processRasterData(double * rasterData, int nXSize, int nYSize);
  void manageRasterIO(GDALRasterBand * band, int nXSize, int nYSize, GDALRWFlag flag, double * rasterMatrix);
public:
  Sample();
  const char * PROCESSED_IMAGE_FILENAME ;
  char * process(char *  productPath, char * destinationPath);
  void translationJP2_GTIFF(char * productPath, char * destinationPath);
};

#endif