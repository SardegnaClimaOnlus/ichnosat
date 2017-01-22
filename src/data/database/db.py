from src.data.logger.logger import logger

from src.data.database.base import Base
import configparser


from sqlalchemy import *
from sqlalchemy.orm import *


class DB:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("src/data/database/config/db.cfg")
        self.engine = create_engine(self.config['database']['connection_string_create'], echo=True, pool_recycle=3600)

    def create_db(self):
        logger.debug("(DB create_db) @@@@@@@@@@@@@@@@@@@@@@@@@@@")
        try:
            conn = self.engine.connect()
            conn.execute("commit")
            conn.execute("create database ichnosat")
            conn.close()
            logger.debug("(DB) Create database")
            engine2 = create_engine(self.config['database']['connection_string'], echo=True, pool_recycle=3600)
            Base.metadata.create_all(engine2)
            return "created_database"
        except Exception as err:
            logger.debug("(DB create_db) Unexpected error:")
            logger.debug(err)
            return False
