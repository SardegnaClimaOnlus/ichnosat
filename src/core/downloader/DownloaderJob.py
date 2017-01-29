#!/usr/bin/env python

from src.data.logger.logger import logger
from src.core.downloader.ConfigurationManager import ConfigurationManager
from src.core.processing_pipe.src.ProcessingPipeManager import ProcessingPipeManager
from src.core.downloader.SearchFilter import SearchFilter
from src.core.downloader.Datasource import Datasource
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import ProductStatus
from src.data.database.entities.product import Product

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class DownloaderJob():
    def __init__(self):
        logger.debug("(DownloaderJob __init__)")
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

    def start(self):
        logger.debug("(Downloader download) <<<<<<<<><><><><>><><><")
        # reload configurations
        logger.debug("(Downloader download) refresh configurations")
        self.refresh_configurations()
        # downloader loop
        logger.debug("(Downloader download) downloader loop")
        for tile in self.configuration.tiles:
            logger.debug("(Downloader download) generate list of available products for tile: " + tile)
            searchFilter = self.create_search_filter(tile)
            # generate products list from search filter
            products_list = self.datasource.get_products_list(searchFilter)
            # add products in database
            for pending_product in products_list:
                self.productService.add_new_product(Product(name=str(pending_product),
                                                            status=ProductStatus.pending))
            products_to_download = self.productService.get_pending_products()
            # download products
            for product in products_to_download:
                self.productService.update_product_status(product.name, ProductStatus.downloading)
                self.datasource.download_product(product.name)
                self.productService.update_product_status(product.name, ProductStatus.downloaded)
                # TODO: add a layer with notifications
                processingPipeManager = ProcessingPipeManager()
                processingPipeManager.start_processing()