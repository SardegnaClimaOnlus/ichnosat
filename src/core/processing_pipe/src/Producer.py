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
from src.core.processing_pipe.src.JobDispatcher import JobDispatcher
from src.data.database.services.products_service import ProductsService

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class Producer():
    def __init__(self, outbox_path, plugins_path):
        logger.info("(Producer __init__) ")
        self.processing = False
        self.outbox_path = outbox_path
        self.plugins_path = plugins_path

    def publish_new_job(self):
        logger.info("(Producer publish_new_job) ")
        logger.info("(Producer publish_new_job) self.processing: " + str(self.processing))
        if self.processing:
            logger.info("(Producer publish_new_job) self.processing is true so return " )
            return
        logger.info("(Producer publish_new_job)  no processing on-going so set self.processing as True")
        self.processing = True
        logger.info("(Producer publish_new_job)  LAUNCH JobDispatcher ")
        job_dispatcher = JobDispatcher(self.outbox_path, self.plugins_path, self)
        job_dispatcher.start()

    def set_processing_false(self):
        logger.debug("(Producer set_processing_false) ")
        self.processing = False






