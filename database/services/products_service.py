from sqlalchemy import *
from sqlalchemy.orm import *
from database.entities.product import Product
from database.entities.product import ProductStatus
import datetime
import logging

class ProductsService():
    def __init__(self):
        engine = create_engine('sqlite:///ichnosat.sqlite', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_new_product(self, product):
        already_present_product = self.session.query(Product). \
            filter(Product.name == product.name).all()
        if(len(already_present_product) == 0):
            self.session.add(product)
            self.session.commit()

    def get_pending_products(self):
        return self.session.query(Product).\
            filter(Product.status == ProductStatus.pending).all()


    def update_product_status(self,product_name,status):
        product =self.session.query(Product). \
            filter(Product.name == product_name).one()
        if product != None:
            product.status = status
            product.last_modify = datetime.datetime.utcnow()
            self.session.commit()

