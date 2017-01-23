import sys
sys.path.append('/usr/ichnosat/')
from src.core.system_manager.system_manager import SystemManager

if __name__ == "__main__":
    # execute only if run as a script
    command = sys.argv[1]
    if command == "run-ichnosat":
        system_manager = SystemManager()
        system_manager.trigger_downloader()