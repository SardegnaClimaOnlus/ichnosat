from src.core.downloader.Configuration import Configuration
from src.core.downloader.ConfigurationManager import ConfigurationManager
from src.core.downloader.SearchFilter import SearchFilter
from src.core.downloader.Datasource import Datasource
from src.data.logger.logger import logger

class Downloader:
    def __init__(self):
        logger.debug("(Downloader __init__)")
        self.configurationManager = ConfigurationManager()
        self.configuration = self.configurationManager.configuration
        self.datasource = Datasource(self.configuration)


    def refresh_configurations(self):
        self.configurationManager.load_configuration()
        self.configuration = self.configurationManager.configuration

    def create_search_filter(self, tile):
        return SearchFilter(tile, self.configuration.start_date, self.configuration.end_date)

    def run(self):
        logger.debug("(Downloader run)")
        # reload configurations
        logger.debug("(Downloader run) reload configurations")
        self.refresh_configurations()
        # downloader loop
        logger.debug("(Downloader run) downloader loop")
        for tile in self.configuration.tiles:
            logger.debug("(Downloader run) generate list of available products for tile: " + tile)
            searchFilter = self.create_search_filter(tile)
            # generate products list from search filter
            products_list = self.datasource.get_products_list(searchFilter)
            # download products
            for product in products_list:
                self.productDownloader.download_product(product)


