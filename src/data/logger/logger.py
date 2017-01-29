#!/usr/bin/env python

import logging
import configparser

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


config = configparser.ConfigParser()
config.read("/usr/ichnosat/src/data/logger/config/logger.cfg")
logging.basicConfig(level=logging.DEBUG,
                    filename=config['DEFAULT']['LogFolder'] + config['DEFAULT']['LogFilename'],
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging