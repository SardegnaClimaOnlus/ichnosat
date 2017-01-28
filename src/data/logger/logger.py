import logging
import configparser

config = configparser.ConfigParser()
config.read("/usr/ichnosat/src/data/logger/config/logger.cfg")
logging.basicConfig(level=logging.INFO,
                    filename=config['DEFAULT']['LogFolder'] + config['DEFAULT']['LogFilename'],
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging