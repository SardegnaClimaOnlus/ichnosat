import threading
from src.core.processing_pipe.src.Job import Job

class JobDispatcher():
    def __init__(self,outbox_path,plugins_path):
        self.queue = []
        self.processing = False
        self.lock = threading.Lock()
        self.outbox_path = outbox_path
        self.plugins_path = plugins_path

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
            product = self.queue.pop()
            job = Job(self.outbox_path, self.plugins_path, product)
            job.run()

        self.lock.acquire()
        self.processing = False
        self.lock.release()

