#!/usr/bin/env python

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from src.data.logger.logger import *
import configparser


from src.data.database.entities.product import Product
from src.data.database.entities.product import ProductStatus

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class ProductsService():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("src/data/database/config/db.cfg")
        self.engine = create_engine(config['database']['connection_string'], echo=True, pool_recycle=3600)

    def add_new_product(self, product):
        result = False
        logger.debug("(ProductsService add_new_product) ")
        logger.debug("(ProductsService add_new_product) product.name: " + product.name)
        logger.debug("(ProductsService add_new_product) product.status: " + str(product.status))
        Session = sessionmaker(bind=self.engine)
        session = Session()
        already_present_product = session.query(Product). \
            filter(Product.name == product.name).all()
        logger.debug("(ProductsService add_new_product) len(already_present_product): >>>>@@@@@@****>>>>>>>>>>>" + str(len(already_present_product)))
        logger.debug("(ProductsService add_new_product) len(already_present_product) == 0: >>>>@@@@@@****>>>>>>>>>>>" + str(len(already_present_product) == 0))

        try:
            if len(already_present_product) == 0:
                session.add(product)
                session.commit()
                result = True
            session.close()
        except Exception as err:
            logger.debug("(ProductsService add_new_product) Unexpected error:")
            logger.debug(err)

        return result

    def get_products_to_process(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloaded).all()
        session.close()
        return result

    def update_product_status(self, product_name, status):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        product = session.query(Product). \
            filter(Product.name == product_name).first()
        if product != None:

            product.status = status
            product.last_modify = datetime.datetime.utcnow()
            session.commit()

        all = session.query(Product).all()
        for product in all:
            logger.debug(str(product))
        session.close()



    def get_pending_products(self):
        logger.debug("(ProductsService get_pending_products)  <<<<<<")
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product).\
            filter(Product.status == ProductStatus.pending).all()
        logger.debug("(ProductsService get_pending_products)  str(len(result))~~~~~~~~~~~~~~O:" + str(len(result)) )
        session.close()
        return result


    def get_downloading_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloading).all()
        session.close()
        return result

    def get_downloaded_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloaded).all()
        session.close()
        return result


    def get_processing_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.processing).all()
        session.close()
        return result


    def get_processed_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.processed).all()
        session.close()
        return result

