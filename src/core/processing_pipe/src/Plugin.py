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
import os, sys, select
from ctypes import *
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import ProductStatus


__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class Plugin():
    """ It is a wrapper of C++ plugin. This class generates the folder of new product and runs the
        dynamic shared libraries (c++ plugins).
    """
    def __init__(self, plugin_name, plugin_path):
        self.productService = ProductsService()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path
        sys.stdout.write(' \b')
        self.pipe_out, pipe_in = os.pipe()
        self.stdout = os.dup(1)
        os.dup2(pipe_in, 1)
        return

    def more_data(self):
        """ Utility method to manage out stream of dynamic shared libraries.
        """
        r, _, _ = select.select([self.pipe_out], [], [], 0)
        return bool(r)

    def read_pipe(self):
        """ Utility method to manage out stream of dynamic shared libraries.
            Reading the out stream pipe.
        """
        while self.more_data():
            logger.debug(os.read(self.pipe_out, 1024).decode('utf-8'))

    def run(self, source, outbox_path):
        """ This method runs the *process* method of dynamic shared library containing the plugin.

            :param source: The path in file system where is located the downloaded file.
            :type source: String

            :param outbox_path: The path of the processed products folder
            :type source: String

            :returns: None
            :rtype: None

        """
        try:
            product_name = source.split('/')[-2]
            destination = outbox_path + product_name + "-" + self.plugin_name + '/'
            if not os.path.exists(destination):
                os.makedirs(destination)
            cdll.LoadLibrary(self.plugin_path)
            libc = CDLL(self.plugin_path)
            product_path = source.encode('utf-8')
            destination_path = destination.encode('utf-8')
            libc.process.argtypes = [c_char_p]
            libc.process(product_path, destination_path)
            os.dup2(self.stdout, 1)
            self.read_pipe()

        except Exception as err:
            logger.warn("Failed scientific-processor plugin with name: " + self.plugin_name)
            logger.debug("(SystemManager set_first_installation_config) Unexpected error:")
            logger.debug(err)
            return False
