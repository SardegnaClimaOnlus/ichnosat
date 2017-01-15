from src.core.downloader.AmazonBucketManager import AmazonBucketManager
from src.core.downloader.ProductDownloader import ProductDownloader
from src.data.logger.logger import logger

class Datasource:
    def __init__(self, configurations):
        logger.debug("(Datasource __init__)")
        self.configurations = configurations
        self.abm = AmazonBucketManager(configurations)
        self.productDownloader = ProductDownloader(configurations.inbox_path,
                                                   configurations.files,
                                                   configurations.aws_domain)
        return

    def get_products_list(self, searchFilter):
        logger.debug("(Datasource get_products_list)")
        products_list = self.abm.get_products_list(searchFilter)
        logger.debug("(Datasrouce get_products_list) list of products:")
        for product_name in products_list:
            logger.debug("(Datasource get_products_list) product_name: " + product_name)
        return products_list

    def download_product(self, product):
        self.productDownloader.download_product(product)
