from logger import logger

class PreProcessor:
    def __init__(self):
        logger.debug('Created new PreProcessor')

    def get_product_from_inbox(self):
        logger.debug('getProductFromInbox()')

    def unzip_product(self):
        logger.debug('unzipProduct()')

    def extract_sensing_time(self):
        logger.debug('extractSensingTime()')

    def extract_tile_id(self):
        logger.debug('extractTileId()')

    def create_new_product_folder(self):
        logger.debug('createNewProductFolder()')

    def move_bands_in_new_product_folder(self):
        logger.debug('moveBandsInNewProductFolder()')


    def move_new_product_to_scientific_processor_inbox(self):
        logger.debug('moveNewProductToScientificProcessorInbox()')

    def notify_new_pre_processor_produc_ready(self):
        logger.debug('notifyNewPreProcessorProductReady()')