import datetime

import enum
from sqlalchemy import *
from sqlalchemy.orm import *

from z_old.database import Base


class ProductStatus(enum.Enum):
    downloading = "downloading"
    pending = "pending"
    downloaded = "downloaded"

class Product(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    status = Column(Enum(ProductStatus))
    last_modify = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Product(name='%s', status='%s', last_modify='%s')>" % (
            self.name, str(self.status), str(self.last_modify))