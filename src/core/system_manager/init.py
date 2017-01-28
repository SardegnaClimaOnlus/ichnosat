import sys
from crontab import CronTab
sys.path.append('/usr/ichnosat/')
import configparser
from src.core.system_manager.system_manager import SystemManager
from src.data.logger.logger import logger


sm = SystemManager()

# compile plugins
sm.compile_plugins()



# set cron tab
config = configparser.ConfigParser()
config_file_path = "/usr/ichnosat/src/core/system_manager/config/config.cfg"

cron = CronTab(user=config['CRON']['user'])
job = cron.new(command=config['CRON']['command'])
job.setall(config['CRON']['cron'])
cron.write()





