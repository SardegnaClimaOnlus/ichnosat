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

import threading
from src.core.processing_pipe.src.Job import Job
from src.data.logger.logger import logger
import queue
from src.data.database.services.products_service import ProductsService
import threading
import configparser

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class JobDispatcher(threading.Thread):
    def __init__(self, outbox_path, plugins_path, delegate):
        logger.info("(JobDispatcher __init__) ")
        self.outbox_path = outbox_path
        self.plugins_path = plugins_path
        self.productService = ProductsService()
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/processing_pipe/config/config.cfg")
        self.delegate = delegate
        threading.Thread.__init__(self)

    def run(self):
        logger.info("(JobDispatcher run) ")
        threads = []
        logger.info("(JobDispatcher run) get list of downloaded products")
        lock = threading.Lock()
        for i in range(int(self.config['PROCESSING_PIPE']['parallel_processing'])):
            logger.info("(JobDispatcher run) SPREAD (" + str(i) + ") thread")
            t = Job(self.outbox_path, self.plugins_path, lock, i)
            t.daemon = True
            t.start()
            threads.append(t)
        logger.info("(JobDispatcher run) SPREAD wait threads end")
        for thread in threads:
            thread.join()
        logger.info("(JobDispatcher run) SPREAD processing ended, set_processing on-going false on DELEGATE")
        self.delegate.set_processing_false()



