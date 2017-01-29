#!/usr/bin/env python

import datetime
import enum
from sqlalchemy import *
from sqlalchemy.orm import *
from src.data.logger.logger import logger
from src.data.database.base import Base

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class ProductStatus(enum.Enum):
    pending = "pending"
    downloading = "downloading"
    downloaded = "downloaded"
    processing = "processing"
    processed = "processed"




class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('products_id_seq'), primary_key=True)
    name = Column(String(50))
    status = Column(Enum(ProductStatus))
    last_modify = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "{\"name\":\"%s\", \"status\":\"%s\", \"last_modify\":\"%s\"}" % (
            self.name, str(self.status), str(self.last_modify))