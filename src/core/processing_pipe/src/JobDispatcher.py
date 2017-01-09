import threading
from src.core.processing_pipe.src.Job import Job

class JobDispatcher():
    def __init__(self):
        self.queue = []
        self.processing = False
        self.lock = threading.Lock()

    def publish_new_job(self, product):
        self.queue.append(product)
        self.dispatch_new_job()

    def dispatch_new_job(self):
        self.lock.acquire()
        if self.processing:
            self.lock.release()
            return
        self.processing = True
        self.lock.release()
        while len(self.queue) > 0:
            # get a product from queue
            product = self.queue.pop()
            # process product
            job = Job(product)
            job.run()
            #self.process_product(product)

        self.lock.acquire()

        self.processing = False
        self.lock.release()

