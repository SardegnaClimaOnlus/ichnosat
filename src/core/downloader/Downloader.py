from src.core.downloader.Configuration import Configuration
from src.core.downloader.ConfigurationManager import ConfigurationManager
from src.core.downloader.SearchFilter import SearchFilter
from src.core.downloader.Datasource import Datasource
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import ProductStatus
from src.data.database.entities.product import Product
from src.data.logger.logger import logger
import threading

class Downloader(threading.Thread):
    def __init__(self):
        logger.debug("(Downloader __init__)")
        threading.Thread.__init__(self)
        self.configurationManager = ConfigurationManager()
        self.configuration = self.configurationManager.get_configuration()
        self.datasource = Datasource(self.configuration)
        self.productService = ProductsService()

    def refresh_configurations(self):
        logger.debug("(Downloader refresh_configurations)")
        self.configurationManager.load_configuration()
        self.configuration = self.configurationManager.configuration
        logger.debug("(Downloader refresh_configurations) finished")

    def create_search_filter(self, tile):
        return SearchFilter(tile, self.configuration.start_date, self.configuration.end_date)

    def run(self):
        logger.debug("(Downloader run)")
        # reload configurations
        logger.debug("(Downloader run) refresh configurations")
        self.refresh_configurations()
        # downloader loop
        logger.debug("(Downloader run) downloader loop")
        for tile in self.configuration.tiles:
            logger.debug("(Downloader run) generate list of available products for tile: " + tile)
            searchFilter = self.create_search_filter(tile)
            # generate products list from search filter
            products_list = self.datasource.get_products_list(searchFilter)
            logger.debug("(Downloader run) products list debug: ")

            # add products in database
            for pending_product in products_list:
                self.productService.add_new_product(Product(name=str(pending_product),
                                                            status=ProductStatus.pending))
            # download products
            for product_name in products_list:
                self.productService.update_product_status(product_name, ProductStatus.downloading)
                self.datasource.download_product(product_name)
                self.productService.update_product_status(product_name, ProductStatus.downloaded)


