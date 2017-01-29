#!/usr/bin/env python

from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"



class Configuration:
    def __init__(self):
        logger.debug("(ConfigurationManager __init__)")
        self.start_date = None
        self.end_date = None
        self.tiles = []
        self.files = []
        self.inbox_path = None

