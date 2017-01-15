import os
import urllib.request
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import *
from src.data.logger.logger import logger

class ProductDownloader:
    def __init__(self, inbox_path, files_to_download,domain):
        self.inbox_path = inbox_path
        self.files_to_download = files_to_download
        self.domain = domain
        return

    def download_product(self, product):
        logger.debug("(ProductDownloader download_product) ")
        logger.debug("(ProductDownloader download_product) product.name: " + product.name)
        new_product_path = self.inbox_path + product.name.replace("/", "-")[:-1]
        if not os.path.exists(new_product_path):
            os.makedirs(new_product_path)

        files_to_download = self.files_to_download.split(',')
        for file_name in files_to_download:
            url = self.domain + product.name + file_name
            new_file_path = new_product_path + '/' + file_name
            urllib.request.urlretrieve(url, new_file_path)
        ps = ProductsService()
        ps.update_product_status(product.name, ProductStatus.downloaded)
        return
