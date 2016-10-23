from logger import logger


class Downloader:
    def __init__(self):
        logger.debug('Created new dowloader')

    def searchNewProducts(self):
        logger.debug('searchNewProduct')

    def downloadProduct(self):
        logger.debug('downloadProduct')

    def sendProductToInbox(self):
        logger.debug('sendProduct')

    def notifyDownloadedNewProduct(self):
        logger.debug('notifyDownloadedNewProduct')