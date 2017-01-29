#!/usr/bin/env python

import subprocess
import logging
import re
import os
import fnmatch
from src.core.processing_pipe.src.Plugin import Plugin
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class PluginManager():
    def __init__(self, plugins_path):
        self.plugins_path = plugins_path

    def get_plugins(self):
        pattern = '*.so'
        plugins = []
        for dName, sdName, fList in os.walk(self.plugins_path):
            for fileName in fList:
                if fnmatch.fnmatch(fileName, pattern):
                    regex_plugin_name = re.escape(dName) + '\/(.*?)\.so'
                    plugin_path = os.path.join(dName, fileName)
                    plugin_name = re.match(regex_plugin_name, plugin_path).group(1)
                    new_plugin = Plugin(plugin_name, plugin_path)
                    plugins.append(new_plugin)
        return plugins

    def compile_plugins(self):
        logger.debug("(PluginManager:compile_plugins) start")
        dirnames = os.listdir(self.plugins_path)
        r = re.compile('^[^\.]')
        dirnames = filter(r.match, dirnames)
        for plugin_name in dirnames:
            try:
                completed_without_error = True
                p = subprocess.Popen(["/bin/bash",
                                      "src/core/system_manager/bash/compile-plugins.sh",
                                      self.plugins_path,
                                      plugin_name,
                                      "var=11; ignore all"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                for line in p.stdout.read().decode('utf-8').split("\n"):
                    if (len(line) > 0):
                        logging.debug("(BASH - compile-plugins.sh): " + line)
                for line in p.stderr.read().decode('utf-8').split("\n"):
                    if (len(line) > 0):
                        logging.debug("[ERROR] (BASH compile-plugins.sh): " + line)
                        completed_without_error = False
                if (completed_without_error):
                    logging.debug("(ichnosat-manager): Completed compile " + plugin_name + " plugin")
                else:
                    logging.debug(
                        "[ERROR] (ichnosat-manager): Failed compilation of scientific_processor plugin '" + plugin_name + "'")
            except ValueError:
                logging.debug(
                    "[ERROR] (ichnosat-manager): Failed compilation of scientific_processor plugin '" + plugin_name + "'")
        logging.debug("(ichnosat-manager): COMPLETED compile scientific_processor plugins")
        return "Done"
