#!/usr/bin/env python

import threading
from src.core.processing_pipe.src.Job import Job
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class JobDispatcher():
    def __init__(self, outbox_path,plugins_path):
        logger.debug("(JobDispatcher __init__) ")
        self.queue = []
        self.processing = False
        self.lock = threading.Lock()
        self.outbox_path = outbox_path
        self.plugins_path = plugins_path

    def publish_new_job(self, product):
        logger.debug("(JobDispatcher publish_new_job) ")
        self.queue.append(product)
        self.dispatch_new_job()

    def dispatch_new_job(self):
        logger.debug("(JobDispatcher dispatch_new_job) ")
        self.lock.acquire()
        if self.processing:
            self.lock.release()
            return
        self.processing = True
        self.lock.release()
        while len(self.queue) > 0:
            product = self.queue.pop()
            job = Job(self.outbox_path, self.plugins_path, product)
            job.run()

        self.lock.acquire()
        self.processing = False
        self.lock.release()

