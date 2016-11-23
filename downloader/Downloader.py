from logger import logger


class Downloader:
    def __init__(self):
        logger.debug('Created new dowloader')

    def search_new_products(self):
        logger.debug('searchNewProduct')

    def download_product(self):
        logger.debug('downloadProduct')

    def send_product_to_inbox(self):
        logger.debug('sendProduct')

    def notify_downloaded_new_product(self):
        logger.debug('notifyDownloadedNewProduct')