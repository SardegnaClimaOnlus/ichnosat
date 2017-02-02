#!/usr/bin/python3

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

from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import Product
from src.data.database.entities.product import ProductStatus
from src.data.logger.logger import logger
from src.core.downloader.DownloaderJob import DownloaderJob
import threading
import queue
from collections import deque
from src.core.downloader.ConfigurationManager import ConfigurationManager
from src.core.downloader.SearchFilter import SearchFilter
from src.core.downloader.Datasource import Datasource



__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class Downloader:
    def __init__(self):
        logger.debug("(Downloader __init__)")
        self.productService = ProductsService()
        self.downloading = False
        self.configurationManager = ConfigurationManager()
        self.configuration = self.configurationManager.get_configuration()
        self.queue = queue.Queue()
        self.pending_tasks = 0
        self.datasource = Datasource(self.configuration)

    def create_search_filter(self, tile):
        return SearchFilter(tile, self.configuration.start_date, self.configuration.end_date)

    def start(self):
        logger.debug("(Downloader run ) ")
        self.pending_tasks += 1

        if self.downloading:
            return
        self.downloading = True

        # retrieve pending products list
        for tile in self.configuration.tiles:
            logger.debug("(Downloader download) generate list of available products for tile: " + tile)
            searchFilter = self.create_search_filter(tile)
            # generate products list from search filter
            products_list = self.datasource.get_products_list(searchFilter)
            # add products in database
            for pending_product in products_list:
                self.productService.add_new_product(Product(name=str(pending_product),
                                                            status=ProductStatus.pending))

        products = [self.queue.put(product) for product in self.productService.get_pending_products()]

        while self.pending_tasks:
            for i in range(3):
                t = DownloaderJob(self.queue)
                t.daemon = True
                t.start()

            self.pending_tasks -= 1
        self.downloading = False
