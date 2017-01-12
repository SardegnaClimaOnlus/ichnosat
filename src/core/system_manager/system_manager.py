from src.data.logger.logger import *

from src.core.processing_pipe.src.PluginManager import PluginManager
from src.core.downloader.start import start_downloader
from src.data.database.db import DB

class SystemManager():
    def compile_plugins(self):
        pm = PluginManager()
        pm.compile_plugins()
        return

    def trigger_downloader(self):
        start_downloader()
        return

    def create_database(self):
        db = DB()
        db.create_db()
        return