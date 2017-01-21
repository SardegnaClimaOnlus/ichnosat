import sys
sys.path.append('/usr/ichnosat/')

import subprocess
from pathlib import Path
from src.core.system_manager.system_manager import SystemManager

import time


sm = SystemManager()

# create database if not exists
# db_file = Path("/usr/ichnosat/data_local/db/ichnosat.sqlite")
# if not db_file.is_file():
#     sm.create_database()

# compile plugins
sm.compile_plugins()


subprocess.Popen(["/bin/bash", "/usr/ichnosat/src/core/system_manager/bash/init.sh", "var=11; ignore all"])

while True:
    time.sleep(10000)

