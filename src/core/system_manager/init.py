import sys
from crontab import CronTab
sys.path.append('/usr/ichnosat/')
from src.core.system_manager.system_manager import SystemManager
from src.data.logger.logger import logger


sm = SystemManager()

# compile plugins
sm.compile_plugins()

# set cron tab
cron = CronTab(user='root')
job = cron.new(command='wget -qO- http://localhost:5000/start-downloader &> /dev/null')
job.setall('10 10 * * *')
cron.write()





