#!/usr/bin/env python

import sys
sys.path.append('/usr/ichnosat/')
from src.core.system_manager.system_manager import SystemManager

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


if __name__ == "__main__":
    # execute only if run as a script
    command = sys.argv[1]
    if command == "run-ichnosat":
        system_manager = SystemManager()
        system_manager.trigger_downloader()