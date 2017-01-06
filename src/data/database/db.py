from src.data.logger.logger import logger

from src.data.database.base import Base
import configparser


from sqlalchemy import *
from sqlalchemy.orm import *


class DB:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("src/data/database/config/db.cfg")
        self.engine = create_engine(self.config['database']['connection_string'], echo=True)

    def create_db(self):
        logger.debug("(DB) Create database")
        Base.metadata.create_all(self.engine)
        return "created_database"