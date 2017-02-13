#!/usr/bin/env python

# ==================================================================================== #
#  __     ______     __  __     __   __     ______     ______     ______     ______
# /\ \   /\  ___\   /\ \_\ \   /\ "-.\ \   /\  __ \   /\  ___\   /\  __ \   /\__  _\
# \ \ \  \ \ \____  \ \  __ \  \ \ \-.  \  \ \ \/\ \  \ \___  \  \ \  __ \  \/_/\ \/
#  \ \_\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\  \ \_\ \_\    \ \_\
#   \/_/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/   \/_/\/_/     \/_/
#
# ==================================================================================== #
#
# Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #

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
    """ This is the manager of plugins, it compiles C++ plugins and retrieve the list of available plugins,
        in ichnosat platform
    """
    def __init__(self, plugins_path):
        self.plugins_path = plugins_path

    def get_plugins(self):
        """ This method retrieve the list of plugins available to process product, via file system
            inspection.

            :returns: list of available plugins in ichnosat platform
            :rtype: List

        """
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
        """ This method compiles  every c++ plugin present in the *plugins* folder of *Processor* module
        """
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
