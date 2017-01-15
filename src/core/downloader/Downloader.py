from src.core.downloader.Configuration import Configuration
from src.core.downloader.ConfigurationManager import ConfigurationManager
from src.core.downloader.SearchFilter import SearchFilter
from src.core.downloader.Datasource import Datasource
from src.core.downloader.ProductDownloader import ProductDownloader

class Downloader:
    def __init__(self):
        self.configurationManager = ConfigurationManager()
        self.configuration = self.configurationManager.configuration
        self.datasource = Datasource()
        self.productDownloader = ProductDownloader()

    def refresh_configurations(self):
        self.configurationManager.load_configuration()
        self.configuration = self.configurationManager.configuration

    def create_search_filter(self):
        sf = SearchFilter()
        return sf;



    def run(self):
        # refresh configurations
        self.refresh_configurations()
        # create filter to generate products list
        searchFilter = self.create_search_filter()
        # get products list with filter
        products_list = self.datasource.get_products_list(searchFilter)
        # download products
        for product in products_list:
            self.productDownloader.download_product(product)


