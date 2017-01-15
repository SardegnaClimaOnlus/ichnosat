from src.data.logger.logger import logger

class Configuration:
    def __init__(self):
        logger.debug("(ConfigurationManager __init__)")
        self.start_date = None
        self.end_date = None
        self.tiles = []
        self.files = []
        self.inbox_path = None

