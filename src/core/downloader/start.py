import datetime
import json
from src.data.logger.logger import logger

import os
import re
import threading
import xml.etree.ElementTree as ET
from collections import OrderedDict
import configparser
import urllib.request
from src.data.database.entities.product import *
from src.data.database.services.products_service import ProductsService
from src.core.downloader.Configuration import Configuration
from src.core.downloader.ConfigurationManager import ConfigurationManager




config = configparser.ConfigParser()
config.read("/usr/ichnosat/src/core/downloader/config/config.cfg")



pending_products = []



def generate_url( tile, year):
    url_template = 'http://sentinel-s2-l1c.s3.amazonaws.com/?list-type=2&prefix=tiles/{tile}/{year}/'
    url = url_template.format(tile=tile, year=year)
    return url

def extract_date(item):
    regex = 'tiles/[0-9]2/[A-Z]/[A-Z]{2}/([0-9]{4})/([0-9]*)/([0-9]*)/'
    match = re.search(regex, item)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    return datetime.date(int(year), int(month), int(day))

class GenerateProductsList(threading.Thread):
    def __init__(self,tile):
        self.tile = tile
        cf = ConfigurationManager()
        self.configuration = cf.configuration

        self.product_list = []
        self.last_item = None
        self.current_year = datetime.datetime.now().year
        super(GenerateProductsList, self).__init__()

    def load_products(self, year, paginated=False):

        # GENERATE URL FOR YEAR
        url = generate_url(self.tile, year)
        # APPEND TO URL START_FROM ATTRIBUTE IF IT IS PAGINATED
        if paginated:
            url = url + "&start-after=" + self.last_item

        # HTTP REQUEST
        response = urllib.request.urlopen(url)
        root = ET.fromstring(response.read().decode('utf-8'))
        # EXTRACT THE DATA FROM XML
        contents = root.findall('{'+config['AWS']['xmlns']+'}Contents')
        for item in contents:
            key = item.find('{' + config['AWS']['xmlns'] + '}Key').text
            product_path = ''
            try:
                product_path = re.search(config['AWS']['products_regex'], key)
            except ValueError:
                logger.error("error parsing")
            self.product_list.append(product_path.group(0))

        # CHECK IF THE PAGE IS TRUNCATED
        if root.find('{' + config['AWS']['xmlns'] + '}IsTruncated').text == 'true':
            self.last_item = contents[-1].find('{' + config['AWS']['xmlns'] + '}Key').text
            return True
        else:
            return False

    def run(self):
        year = int(self.configuration.start_date.year)

        # EXTRACT WHOLE LIST OF PRODUCT VIA AMAZON, FROM START_YEAR to TODAY
        while year <= self.current_year:
            logger.debug("year: " + str(year))
            isTruncated = self.load_products(year, False)
            while isTruncated:
                isTruncated = self.load_products(year, True)
            year += 1

        # CLEAN LIST OF PRODUCTS
        self.product_list = set(self.product_list)

        # GENERATE DICTIONARY
        dict = {}
        for product in self.product_list:
            date = extract_date(str(product))
            product_string = str(product)
            dict[date] = product_string

        # ORDER DICTIONARY
        dict = OrderedDict(sorted(dict.items()))

        # FILTER BY DATE INTERVAL
        for product_date in dict:
            if product_date >= self.configuration.start_date and product_date <= self.configuration.end_date:
                pending_products.append(dict[product_date])


def downloadProduct(product_name):
    new_product_path = config['DOWNLOADER']['inbox_path'] + product_name.replace("/", "-")[:-1]
    if not os.path.exists(new_product_path):
        os.makedirs(new_product_path)

    files_to_download=config['DOWNLOADER']['files_to_download'].split(',')
    for file_name in files_to_download:
        url = "http://sentinel-s2-l1c.s3.amazonaws.com/" + product_name + file_name
        new_file_path = new_product_path + '/' +file_name
        urllib.request.urlretrieve(url, new_file_path)
        logger.debug("DOWNLOADED FILE WITH PATH ********>>>>> " + new_file_path)
    ps = ProductsService()
    ps.update_product_status(product_name, ProductStatus.downloaded)
    return


def start_downloader():
    ps = ProductsService()

    # GENERATE PRODUCT LIST
    threads = []

    for tile in config['FILTER']['tiles'].split(','):
        task = GenerateProductsList(tile)
        threads.append(task)
        task.start()

    # WAIT ALL THREADS
    for thread in threads:
        thread.join()

    for pending_product in pending_products:
        ps.add_new_product(Product(name=str(pending_product),
                                   status=ProductStatus.pending))

    # DOWNLOAD PRODUCTS
    for product in ps.get_pending_products():
        downloadProduct(product.name)




if __name__ == '__main__':
    start()



