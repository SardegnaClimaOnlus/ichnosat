from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from database.base import Base
from database.entities.product import Product
import logging


class DB:
    def create_db(self):

        logging.debug("(DB) Create database")
        engine = create_engine('sqlite:///ichnosat.sqlite', echo=True)
        Base.metadata.create_all(engine)

        return "created_database"