import subprocess
from pathlib import Path
from src.core.system_manager.system_manager import SystemManager

# initialize system
db_file = Path("/usr/ichnosat/data_local/db/ichnosat.sqlite")
if not db_file.is_file():
    sm = SystemManager()
    sm.create_database()