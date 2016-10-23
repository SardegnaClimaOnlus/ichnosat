from logger import logger

class PostProcessor:
    def __init__(self):
        logger.debug('Created new PostProcessor')

    def getNewProduct(self):
        logger.debug('getNewProduct()')

    def createNetcdfFromProduct(self):
        logger.debug('createNetcdfFromProduct')

    def moveNewNetcdfToArchive(self):
        logger.debug('moveNewNetcdfToArchive')
