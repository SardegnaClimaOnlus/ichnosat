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

from src.core.processing_pipe.src.PluginManager import PluginManager
from src.data.logger.logger import logger
import shutil

from src.data.database.entities.product import ProductStatus
import threading
from src.data.logger.logger import logger
from src.data.database.services.products_service import ProductsService
import time

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class Job(threading.Thread):
    def __init__(self, outbox_path, plugins_path, lock, i):
        self.i = i
        logger.info("(Job __init__) ["+str(self.i)+"]")
        self.lock = lock
        self.outbox_path = outbox_path
        plugin_manager = PluginManager(plugins_path)
        self.plugins = plugin_manager.get_plugins()
        self.productService = ProductsService()
        threading.Thread.__init__(self)

        return

    def fibonacci(self, max_value):
        i, j = 2, 3
        while i < max_value:
            yield i
            i, j = j, i + j

    def _process(self, product):
        logger.info("(Job _process) ["+str(self.i)+"] process the product with name: " + product.name)
        original_name = product.name.replace("/", "-")
        source = "/usr/ichnosat/data_local/inbox/" + original_name[:-1] + "/"

        logger.info("(Job run)["+str(self.i)+"] process product with path: " + source)
        for plugin in self.plugins:
            plugin.run(source, self.outbox_path)
        self.productService.update_product_status(product.name, ProductStatus.processed)
        logger.info("(Job run) ["+str(self.i)+"]remove product with path > " + source)
        shutil.rmtree(source)

    def run(self):
        WAIT_MULTIPLICATOR = 0.5
        SECONDS_PER_MINUTE = 60
        FIBONACCI_ITERATIONS = 1000
        logger.info("(Job run)["+str(self.i)+"] ")
        iterator = self.fibonacci(FIBONACCI_ITERATIONS)
        while True:
            total_wait_time = 0
            logger.info("(Job run) ["+str(self.i)+"]@ Acquire the lock")
            self.lock.acquire()
            logger.info("(Job run)["+str(self.i)+"] @ Get a downloaded product from db")
            product = self.productService.get_a_downloaded_product()
            logger.info("(Job run) ["+str(self.i)+"]@ Extracted downloaded product " + str(product))
            if product:
                logger.info("(Job run) ["+str(self.i)+"]@ found a product to process")
                self.productService.update_product_status(product.name, ProductStatus.processing)
                self.lock.release()
                self._process(product)
                del iterator
                iterator = self.fibonacci(FIBONACCI_ITERATIONS)
            else:
                logger.info("(Job run) ["+str(self.i)+"]@ not found a product, relase the lock")
                self.lock.release()
                try:
                    logger.info("(Job run) ["+str(self.i)+"]@ Iteration")
                    n = next(iterator)
                    wait_seconds = n * WAIT_MULTIPLICATOR
                    total_wait_time += wait_seconds
                    time.sleep(wait_seconds)
                    logger.info(" (Job run) ["+str(self.i)+"] ---- > waited " + str(total_wait_time) +
                          " seconds, " + str(total_wait_time / SECONDS_PER_MINUTE) +
                          " minutes in total")
                    continue
                except StopIteration:
                    logger.info("(Job run) ["+str(self.i)+"]@ Iteration attempts finished, return")
                    del iterator
                    break






