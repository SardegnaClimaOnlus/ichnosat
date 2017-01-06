import logging

from database.base import Base
from sqlalchemy import *
from sqlalchemy.orm import *


class DB:
    def create_db(self):

        logging.debug("(DB) Create database")
        engine = create_engine('sqlite:///ichnosat.sqlite', echo=True)
        Base.metadata.create_all(engine)

        return "created_database"