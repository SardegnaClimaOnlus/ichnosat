import unittest  # second tests
from src.core.downloader.AmazonBucketManager import AmazonBucketManager


class AmazonBucketManagerTestCase(unittest.TestCase):

    def test_generate_url(self):
        amazon_bucket_manager = AmazonBucketManager(None)
        result = amazon_bucket_manager.generate_url("tile_string", "year_string")
        aspected = "http://sentinel-s2-l1c.s3.amazonaws.com/?list-type=2&prefix=tiles/tile_string/year_string/"
        self.assertEqual(result, aspected)


    def test_extract_date(self):
        amazon_bucket_manager = AmazonBucketManager(None)
        tile_string = "tiles/32/T/MK/2012/07/13/"
        date = amazon_bucket_manager.extract_date(tile_string)
        self.assertEqual(2012, date.year)
        self.assertEqual(7, date.month)
        self.assertEqual(13, date.day)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AmazonBucketManagerTestCase())

    return suite


if __name__ == '__main__':
    unittest.main()
