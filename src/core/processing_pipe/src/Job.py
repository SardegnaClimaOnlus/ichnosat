from src.core.processing_pipe.src.PluginManager import PluginManager
from src.data.logger.logger import logger

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
