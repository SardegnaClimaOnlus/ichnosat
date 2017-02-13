#!/usr/bin/env python

# ==================================================================================== #
#  __     ______     __  __     __   __     ______     ______     ______     ______
# /\ \   /\  ___\   /\ \_\ \   /\ "-.\ \   /\  __ \   /\  ___\   /\  __ \   /\__  _\
# \ \ \  \ \ \____  \ \  __ \  \ \ \-.  \  \ \ \/\ \  \ \___  \  \ \  __ \  \/_/\ \/
#  \ \_\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\  \ \_\ \_\    \ \_\
#   \/_/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/   \/_/\/_/     \/_/
#
# ==================================================================================== #
#
# Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #

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
    """ It is the entry point of the *Processor*, handling the processing requests triggered by the *Downloader*
    """
    def __init__(self):
        logger.debug("(ProcessingPipeManager __init__) ")
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/processing_pipe/config/config.cfg")

    def process_product(self, product_name):
        """ This method is the wrapper of the web request to trigger a new processing task.

            :param product_name: The name of the product to process
            :type product_name: String

        """
        logger.debug("(ProcessingPipeManager process_product) ")
        product_path = self.config['FOLDERS']['inbox_path'] + product_name.replace("/", "-")[:-1]
        self.notify_to_scientific_processor(product_path + '/')

    def notify_to_scientific_processor(self, file_path):
        """ This method launches the http request to trigger a new processing process.
            It represent the networking interface to the scientific processor.

            :param file_path: The path where is located the product to process
            :type file_path: String

        """
        logger.debug("(ProcessingPipeManager notify_to_scientific_processor) ")
        body = {"path": file_path}
        params = json.dumps(body).encode('utf8')
        req = urllib.request.Request("http://localhost:5002/process",
                                     data=params,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)

    def start_processing(self):
        """ The entry point of the *ProcessingPipeManager* class.
        """
        logger.debug("(ProcessingPipeManager start_processing) ")
        ps = ProductsService()
        for product in ps.get_products_to_process():
            self.process_product(product.name)

