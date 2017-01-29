#!/usr/bin/env python

import sys
from crontab import CronTab
sys.path.append('/usr/ichnosat/')
import configparser
from src.core.system_manager.system_manager import SystemManager
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"



sm = SystemManager()

# compile plugins
sm.compile_plugins()



# set cron tab
config = configparser.ConfigParser()
config_file_path = "/usr/ichnosat/src/core/system_manager/config/config.cfg"
config.read(config_file_path)

cron = CronTab(user=config['CRON']['user'])
job = cron.new(command=config['CRON']['command'])
job.setall(config['CRON']['cron'])
cron.write()





