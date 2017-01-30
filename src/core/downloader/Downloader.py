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

from src.data.database.services.products_service import ProductsService
from src.data.logger.logger import logger
from src.core.downloader.DownloaderJob import DownloaderJob
import threading

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class Downloader():
    def __init__(self):
        logger.debug("(Downloader __init__)")
        self.productService = ProductsService()
        self.pending_tasks = 0
        self.lock = threading.Lock()
        self.downloading = False

    def start(self):
        logger.debug("(Downloader run ) ")
        logger.debug("(Downloader run ) self.pending_tasks: " + str(self.pending_tasks))
        self.pending_tasks += 1
        self.lock.acquire()
        if self.downloading:
            logger.debug("(Downloader run ) ANOTHER DOWNLOADING PROCESS IN PROGRESS! ")
            self.lock.release()
            logger.debug("(Downloader run ) ANOTHER DOWNLOADING PROCESS IN PROGRESS! >>> RETURN ")
            return
        self.downloading = True
        self.lock.release()
        while self.pending_tasks:
            logger.debug("(Downloader run ) LOOP : DOWNLOAD ")
            downloader_job = DownloaderJob()
            downloader_job.start()
            self.pending_tasks -= 1
        self.lock.acquire()
        self.downloading = False
        self.lock.release()

