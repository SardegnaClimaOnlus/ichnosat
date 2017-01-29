#!/usr/bin/env python

from src.data.logger.logger import logger
from src.data.database.services.products_service import ProductsService
import urllib.request
import json
import configparser

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class ProcessingPipeManager:
    def __init__(self):
        logger.debug("(ProcessingPipeManager __init__) ")
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/processing_pipe/config/config.cfg")

    def process_product(self, product_name):
        logger.debug("(ProcessingPipeManager process_product) ")
        product_path = self.config['FOLDERS']['inbox_path'] + product_name.replace("/", "-")[:-1]
        self.notify_to_scientific_processor(product_path + '/')

    def notify_to_scientific_processor(self, file_path):
        logger.debug("(ProcessingPipeManager notify_to_scientific_processor) ")
        body = {"path": file_path}
        params = json.dumps(body).encode('utf8')
        req = urllib.request.Request("http://localhost:5002/process",
                                     data=params,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)

    def start_processing(self):
        logger.debug("(ProcessingPipeManager start_processing) ")
        logger.debug(">>>>>>>>>>>> BEFORE THE PROCESSING LOOP")
        ps = ProductsService()
        for product in ps.get_products_to_process():
            logger.debug("-----> indaloop:  product.name: " + product.name)
            self.process_product(product.name)

