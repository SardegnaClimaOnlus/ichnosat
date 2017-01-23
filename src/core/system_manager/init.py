import sys

sys.path.append('/usr/ichnosat/')
from apscheduler.schedulers.background import BackgroundScheduler
import urllib.request
import subprocess
from src.data.logger.logger import logger

from src.core.system_manager.system_manager import SystemManager
import time

sm = SystemManager()

# compile plugins
sm.compile_plugins()
# set cron tab

def tick():
    logger.debug("+++++>>>>>+++++++>>>>>>>++++++>>>> (system_manager minute_schedule)")
    urllib.request.urlretrieve("http://localhost:5000/start-downloader")


scheduler = BackgroundScheduler()
scheduler.add_job(tick, 'interval', seconds=3)
scheduler.start()

# run init.sh
# subprocess.Popen(["/bin/bash", "/usr/ichnosat/src/core/system_manager/bash/init.sh", "var=11; ignore all"])
#
#
# while True:
#     time.sleep(10000)



