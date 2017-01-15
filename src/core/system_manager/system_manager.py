from src.data.logger.logger import logger

from src.core.processing_pipe.src.PluginManager import PluginManager
#from src.core.downloader.start import start_downloader
from src.core.downloader.Downloader import Downloader
from src.data.database.db import DB
from src.core.processing_pipe.src.ProcessingPipeManager import ProcessingPipeManager
import configparser

class SystemManager():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/system_manager/config/config.cfg")
        self.ppm = ProcessingPipeManager()
        self.pluginManager = PluginManager(self.config['PATHS']['plugins'])


    def compile_plugins(self):
        self.pluginManager.compile_plugins()

    def trigger_downloader(self):
        #start_downloader()
        downloader = Downloader()
        downloader.run()
        self.ppm.start_processing()

    def create_database(self):
        db = DB()
        db.create_db()