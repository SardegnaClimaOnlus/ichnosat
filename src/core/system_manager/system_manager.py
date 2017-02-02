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
from src.core.processing_pipe.src.PluginManager import PluginManager
from src.core.downloader.Downloader import Downloader
from src.data.database.db import DB
from src.core.processing_pipe.src.ProcessingPipeManager import ProcessingPipeManager
import configparser
from src.data.database.services.products_service import ProductsService
from src.data.database.services.products_service import ProductStatus

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class SystemManager():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file_path = "/usr/ichnosat/src/core/system_manager/config/config.cfg"
        self.ProcessingPipeManager = ProcessingPipeManager()
        self.config.read(self.config_file_path)
        self.pluginManager = PluginManager(self.config['PATHS']['plugins'])
        self.productService = ProductsService()
        self.downloader = Downloader()

    def compile_plugins(self):
        self.pluginManager.compile_plugins()

    def trigger_downloader(self):
        logger.debug("(SystemManager trigger_downloader) ")
        logger.debug("(SystemManager trigger_downloader) call downloader ")
        try:
            self.downloader.start()
        except Exception as err:
            logger.debug("(SystemManager trigger_downloader) Unexpeted error:")
            logger.debug(err)


    def create_database(self):
        try:
            db = DB()
            db.create_db()
            return True
        except Exception as err:
            logger.debug("(SystemManager create_database) Unexpected error:")
            logger.debug(err)
            return False

    def fix_inconsistent_data_in_db(self):
        downloading_products = self.productService.get_downloading_products()
        for product in downloading_products:
            self.productService.update_product_status(product.name, ProductStatus.pending)
        processing_products = self.productService.get_processing_products()
        for product in processing_products :
            self.productService.update_product_status(product.name, ProductStatus.downloaded)



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

    def is_first_installation(self):
        self.config.read(self.config_file_path)
        return True if self.config['SYSTEM_STATUS']['first_installation'] == 'true' else False

    def set_first_installation_config(self, new_status):
        try:
            value = 'true' if new_status else 'false'
            config = configparser.RawConfigParser()
            config.read(self.config_file_path)
            config.set('SYSTEM_STATUS', 'first_installation', value)
            with open(self.config_file_path, 'w') as configfile:
                config.write(configfile)
            return True
        except Exception as err:
            logger.debug("(SystemManager set_first_installation_config) Unexpected error:")
            logger.debug(err)
            return False





