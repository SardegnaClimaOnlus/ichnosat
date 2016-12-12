import logging
import configparser

config = configparser.ConfigParser()
config.read("config/config.cfg")
logging.basicConfig(level=logging.DEBUG, filename=config['DEFAULT']['LogFolder'] + config['DEFAULT']['LogFilename'],format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

