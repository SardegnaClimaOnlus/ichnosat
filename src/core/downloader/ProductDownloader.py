#!/usr/bin/env python

import os
import urllib.request
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import *
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class ProductDownloader:
    def __init__(self, inbox_path, files_to_download, domain):
        logger.debug("(ProductDownloader __init__) ")
        self.inbox_path = inbox_path
        self.files_to_download = files_to_download

        self.domain = domain
        return

    def download_product(self, product_name):
        logger.debug("(ProductDownloader download_product) ")
        logger.debug("(ProductDownloader download_product) product.name: " + product_name)
        new_product_path = self.inbox_path + product_name.replace("/", "-")[:-1]
        if not os.path.exists(new_product_path):
            os.makedirs(new_product_path)
        files_to_download = self.files_to_download #.split(',')
        for file_name in files_to_download:
            url = self.domain + product_name + file_name
            new_file_path = new_product_path + '/' + file_name
            urllib.request.urlretrieve(url, new_file_path)


        return
