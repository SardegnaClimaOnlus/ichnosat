#!/usr/bin/env python

from src.core.processing_pipe.src.PluginManager import PluginManager
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class Job():
    def __init__(self, outbox_path, plugins_path, source):
        self.source = source
        self.outbox_path = outbox_path
        plugin_manager = PluginManager(plugins_path)
        self.plugins = plugin_manager.get_plugins()
        return

    def run(self):
        for plugin in self.plugins:
            plugin.run(self.source, self.outbox_path)
