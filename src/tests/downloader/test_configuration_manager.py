import unittest  # second tests
from src.core.downloader.ConfigurationManager import ConfigurationManager


class ConfigurationManagerTestCase(unittest.TestCase):

    def test_datetime_from_string(self):
        configuration_manager = ConfigurationManager()
        date = configuration_manager.datetime_from_string("2012/07/13")
        self.assertEqual(2012, date.year)
        self.assertEqual(7, date.month)
        self.assertEqual(13, date.day)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ConfigurationManagerTestCase())

    return suite


if __name__ == '__main__':
    unittest.main()
