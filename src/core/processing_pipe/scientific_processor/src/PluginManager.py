import subprocess
import logging
import re
import os


class PluginManager():
    def compile_plugins(self):
        dirnames = os.listdir('/usr/ichnosat/src/core/processing_pipe/scientific_processor/src/plugins/')
        r = re.compile('^[^\.]')
        dirnames = filter(r.match, dirnames)

        for plugin_name in dirnames:
            try:
                completed_without_error = True
                logging.debug("(ichnosat-manager): START compile of scientific-plugin '" + plugin_name + "' plugin")
                p = subprocess.Popen(["/bin/bash", "bash/compile-plugins.sh", plugin_name, "var=11; ignore all"],
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