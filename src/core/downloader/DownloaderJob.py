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
from src.core.downloader.ConfigurationManager import ConfigurationManager
from src.core.processing_pipe.src.ProcessingPipeManager import ProcessingPipeManager
from src.core.downloader.SearchFilter import SearchFilter
from src.core.downloader.Datasource import Datasource
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import ProductStatus
from src.data.database.entities.product import Product
import threading
import queue

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class DownloaderJob(threading.Thread):
    def __init__(self, queue):
        logger.debug("(DownloaderJob __init__)")
        self.configurationManager = ConfigurationManager()
        self.configuration = self.configurationManager.get_configuration()
        self.datasource = Datasource(self.configuration)
        self.productService = ProductsService()
        self.queue = queue
        threading.Thread.__init__(self)

    def refresh_configurations(self):
        logger.debug("(Downloader refresh_configurations)")
        self.configurationManager.load_configuration()
        self.configuration = self.configurationManager.configuration
        logger.debug("(Downloader refresh_configurations) finished")

    def run(self):
        while True:
            try:
                if self.queue.qsize():
                    product = self.queue.get()
                    self.productService.update_product_status(product.name, ProductStatus.downloading)
                    self.queue.task_done()
                    self.datasource.download_product(product.name)
                    self.productService.update_product_status(product.name, ProductStatus.downloaded)
                    processing_pipe_manager = ProcessingPipeManager()
                    processing_pipe_manager.start_processing()
                else:
                    return
            except queue.Empty:
                break
            else:
                # Handle task here and call q.task_done()
                pass



