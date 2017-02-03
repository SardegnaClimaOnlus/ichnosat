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
import queue
from src.data.database.entities.product import ProductStatus
import threading
from src.data.logger.logger import logger
from src.data.database.services.products_service import ProductsService

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class Job(threading.Thread):
    def __init__(self, outbox_path, plugins_path, queue):
        logger.info("(Job __init__) ")
        self.queue = queue
        self.outbox_path = outbox_path
        plugin_manager = PluginManager(plugins_path)
        self.plugins = plugin_manager.get_plugins()
        self.productService = ProductsService()
        threading.Thread.__init__(self)
        return

    def run(self):
        logger.info("(Job run) ")
        while True:
            try:
                logger.info("(Job run) in the queue there are " + str(self.queue.qsize()) + " items")
                if self.queue.qsize():
                    logger.info("(Job run) get a product from queue")
                    product = self.queue.get()
                    original_name = product.name.replace("/", "-")
                    source = "/usr/ichnosat/data_local/inbox/" + original_name[:-1] + "/"
                    self.productService.update_product_status(product.name, ProductStatus.processing)
                    self.queue.task_done()
                    logger.info("(Job run) PROCESS PRODUCT WITH PATH -------: " + source)
                    for plugin in self.plugins:
                        plugin.run(source, self.outbox_path)
                    self.productService.update_product_status(product.name, ProductStatus.processed)
                    logger.info("(Job run) REMOVE PRODUCT WITH PATH > " + source)
                    shutil.rmtree(source)
                else:
                    return
            except queue.Empty:
                logger.info("(Job run) THE QUEUE IS EMTPY EXIT")
                self.queue.task_done()
                break
            else:
                pass



