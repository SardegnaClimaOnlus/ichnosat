import sys
from crontab import CronTab
sys.path.append('/usr/ichnosat/')

import subprocess

from src.core.system_manager.system_manager import SystemManager
import time

sm = SystemManager()

# compile plugins
sm.compile_plugins()
# set cron tab
cron = CronTab(user=True)
job = cron.new(command='wget http://localhost:5000/start-downloader')
job.setall('00 23 * * *')
cron.write()

# run init.sh
# subprocess.Popen(["/bin/bash", "/usr/ichnosat/src/core/system_manager/bash/init.sh", "var=11; ignore all"])
#
#
# while True:
#     time.sleep(10000)



