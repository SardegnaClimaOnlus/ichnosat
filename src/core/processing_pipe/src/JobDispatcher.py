import threading
from src.core.processing_pipe.src.Job import Job
from src.data.logger.logger import logger

class JobDispatcher():
    def __init__(self,outbox_path,plugins_path):
        self.queue = []
        self.processing = False
        self.lock = threading.Lock()
        self.outbox_path = outbox_path
        self.plugins_path = plugins_path

    def publish_new_job(self, product):
        logger.debug("publish_new_job <<<<<<<<<<<")
        logger.debug("product: " + product)
        self.queue.append(product)
        self.dispatch_new_job()

    def dispatch_new_job(self):
        logger.debug("Dispatch new job <<<<<<<<<<<")
        self.lock.acquire()
        if self.processing:
            self.lock.release()
            return
        self.processing = True
        self.lock.release()
        logger.debug("len(self.queue): " + str(len(self.queue)))
        while len(self.queue) > 0:
            logger.debug("----- inside the loop -----")
            product = self.queue.pop()
            logger.debug("product: " + product)
            logger.debug("self.outbox_path: " + self.outbox_path)
            logger.debug("self.plugins_path: " + self.plugins_path)
            job = Job(self.outbox_path, self.plugins_path, product)
            job.run()

        self.lock.acquire()
        self.processing = False
        self.lock.release()

