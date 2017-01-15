import subprocess
from pathlib import Path
from src.core.system_manager.system_manager import SystemManager


sm = SystemManager()

# create database if not exists
db_file = Path("/usr/ichnosat/data_local/db/ichnosat.sqlite")
if not db_file.is_file():
    sm.create_database()

# compile plugins
sm.compile_plugins()


