
import logging


def test():
    logging.debug('HELLO FROM DOWNLOADER')

class Downloader:
    def __init__(self):
        logging.debug('Created new dowloader')

    def search_new_products(self):
        logging.debug('searchNewProduct')

    def download_product(self):
        logging.debug('downloadProduct')

    def send_product_to_inbox(self):
        logging.debug('sendProduct')

    def notify_downloaded_new_product(self):
        logging.debug('notifyDownloadedNewProduct')