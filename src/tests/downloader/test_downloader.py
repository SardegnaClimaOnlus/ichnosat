import unittest  # second tests
from src.core.downloader.AmazonBucketManager import AmazonBucketManager


class ConfigTestCase(unittest.TestCase):

    def test_generate_url(self):
        amazon_bucket_manager = AmazonBucketManager(None)
        result = amazon_bucket_manager.generate_url("tile_string", "year_string")
        aspected = "http://sentinel-s2-l1c.s3.amazonaws.com/?list-type=2&prefix=tiles/tile_string/year_string/"
        self.assertEqual(result, aspected)


    def setUp(self):
        print('stp')

    def runTest(self):
        print('stp')

    def test(self):
        self.assertTrue(True)

    def test_isupper(self):
        self.assertFalse('FOOd'.isupper())

    def test_isupper2(self):
        self.assertTrue('FOO'.isupper())

    def setUp(self):
        print("before tests method")

    def tearDown(self):
        print("after tests method")

    @classmethod
    def setUpClass(self):
        print("before tests class")

    @classmethod
    def tearDownClass(self):
        print("after tests class")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ConfigTestCase())

    return suite


if __name__ == '__main__':
    unittest.main()
