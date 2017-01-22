import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from src.data.logger.logger import *
import configparser


from src.data.database.entities.product import Product
from src.data.database.entities.product import ProductStatus



class ProductsService():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("src/data/database/config/db.cfg")
        engine = create_engine(config['database']['connection_string'], echo=True, pool_recycle=3600)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_new_product(self, product):
        logger.debug("(ProductsService add_new_product) ")
        logger.debug("(ProductsService add_new_product) product.name: " + product.name)
        already_present_product = self.session.query(Product). \
            filter(Product.name == product.name).all()
        if(len(already_present_product) == 0):
            self.session.add(product)
            self.session.commit()

    def get_pending_products(self):
        return self.session.query(Product).\
            filter(Product.status == ProductStatus.pending).all()

    def get_products_to_process(self):
        return self.session.query(Product). \
            filter(Product.status == ProductStatus.downloaded ).all()

    def update_product_status(self, product_name, status):
        product = self.session.query(Product). \
            filter(Product.name == product_name).first()
        if product != None:

            product.status = status
            product.last_modify = datetime.datetime.utcnow()
            self.session.commit()

        all = self.session.query(Product).all()
        for product in all:
            logger.debug(str(product))



    def get_pending_products(self):
        return self.session.query(Product).\
            filter(Product.status == ProductStatus.pending).all()



    def get_downloading_products(self):
        return self.session.query(Product). \
            filter(Product.status == ProductStatus.downloading).all()

    def get_downloaded_products(self):
        return self.session.query(Product). \
            filter(Product.status == ProductStatus.downloaded).all()


    def get_processing_products(self):
        return self.session.query(Product). \
            filter(Product.status == ProductStatus.processing).all()


    def get_processed_products(self):
        return self.session.query(Product). \
            filter(Product.status == ProductStatus.processed).all()


