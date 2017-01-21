from src.data.logger.logger import logger

from src.core.processing_pipe.src.PluginManager import PluginManager
#from src.core.downloader.start import start_downloader
from src.core.downloader.Downloader import Downloader
from src.data.database.db import DB
from src.core.processing_pipe.src.ProcessingPipeManager import ProcessingPipeManager
import configparser
from src.data.database.services.products_service import ProductsService

class SystemManager():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/system_manager/config/config.cfg")
        self.ProcessingPipeManager = ProcessingPipeManager()
        self.pluginManager = PluginManager(self.config['PATHS']['plugins'])
        self.productService = ProductsService()


    def compile_plugins(self):
        self.pluginManager.compile_plugins()

    def trigger_downloader(self):
        logger.debug("(SystemManager trigger_downloader) ")
        logger.debug("(SystemManager get_pending_products) call downloader ")
        downloader = Downloader()
        downloader.start()
        logger.debug("(SystemManager get_pending_products) call processing")
        self.ProcessingPipeManager.start_processing()

    def create_database(self):
        db = DB()
        db.create_db()

    def get_pending_products(self):
        logger.debug("(SystemManager get_pending_products) ")
        return self.productService.get_pending_products()

    def get_downloading_products(self):
        return self.productService.get_downloading_products()

    def get_downloaded_products(self):
        return self.productService.get_downloaded_products()

    def get_processing_products(self):
        return self.productService.get_processing_products()

    def get_processed_products(self):
        return self.productService.get_processed_products()