from logger import logger

class PostProcessor:
    def __init__(self):
        logger.debug('Created new PostProcessor')

    def get_new_product(self):
        logger.debug('getNewProduct()')

    def create_netcdf_from_product(self):
        logger.debug('createNetcdfFromProduct')

    def move_new_netcdf_to_archive(self):
        logger.debug('moveNewNetcdfToArchive')
