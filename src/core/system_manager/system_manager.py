from src.data.logger.logger import logger

from src.core.processing_pipe.src.PluginManager import PluginManager
from src.core.downloader.start import start_downloader
from src.data.database.db import DB

class SystemManager():
    def compile_plugins(self):
        logger.debug("(SystemManager:compile_plugins) start compile_plugins")
        pm = PluginManager("/usr/ichnosat/src/core/processing_pipe/scientific_processor/src/plugins")
        logger.debug(">>>> here")
        #TODO: create a loop with an array from config file
        pm.compile_plugins()
        return

    def trigger_downloader(self):
        start_downloader()
        return

    def create_database(self):
        db = DB()
        db.create_db()
        return