from src.data.database.services.products_service import ProductsService
from src.data.logger.logger import logger
from src.core.downloader.DownloaderJob import DownloaderJob
import threading

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

