import datetime
import json
from src.data.logger.logger import *
import logging
import os
import re
import threading
import xml.etree.ElementTree as ET
from collections import OrderedDict
import configparser
import urllib.request
from src.data.database.entities.product import *
from src.data.database.services.products_service import ProductsService


config = configparser.ConfigParser()
config.read("downloader/config/logger.cfg")

# TODO: to move this variable into class property
pending_products = []

def callback():
    logging.debug("hello from scheduler")

def generate_url( tile, year):
    logging.debug("(Downloader, generate_url) START")
    # TODO: move this string to configuration file
    url_template = 'http://sentinel-s2-l1c.s3.amazonaws.com/?list-type=2&prefix=tiles/{tile}/{year}/'
    url = url_template.format(tile=tile, year=year)
    logging.debug('url: ' + url)
    logging.debug("(Downloader, generate_url) END")
    return url

def extract_date(item):
    # TODO: move this string to configuration file
    regex = 'tiles/[0-9]2/[A-Z]/[A-Z]{2}/([0-9]{4})/([0-9]*)/([0-9]*)/'
    match = re.search(regex, item)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    return datetime.date(int(year), int(month), int(day))

class GenerateProductsList(threading.Thread):
    def __init__(self, tile, start_date, end_date):
        date_regex = "([0-9]*)/([0-9]*)/([0-9]*)"
        start_date_match = re.search(date_regex, start_date)
        if end_date != 'NOW':
            end_date_match = re.search(date_regex, end_date)
            self.end_date = datetime.date(int(end_date_match.group(1)),
                                          int(end_date_match.group(2)),
                                          int(end_date_match.group(3)))
        else:
            self.end_date = datetime.datetime.now().date()
        self.tile = tile
        self.start_year = start_date_match.group(1)
        self.start_month = start_date_match.group(2)
        self.start_day = start_date_match.group(3)
        self.product_list = []
        self.last_item = None
        self.current_year = datetime.datetime.now().year
        logging.debug("CURRENT YEAR: " + str(self.current_year))
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
                logging.error("error parsing")
            self.product_list.append(product_path.group(0))

        # CHECK IF THE PAGE IS TRUNCATED
        if root.find('{' + config['AWS']['xmlns'] + '}IsTruncated').text == 'true':
            self.last_item = contents[-1].find('{' + config['AWS']['xmlns'] + '}Key').text
            return True
        else:
            return False

    def run(self):
        year = int(self.start_year)

        # EXTRACT WHOLE LIST OF PRODUCT VIA AMAZON, FROM START_YEAR to TODAY
        while year <= self.current_year:
            logging.debug("year: " + str(year))
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
        start_date = datetime.date(int(self.start_year), int(self.start_month), int(self.start_day))
        for product_date in dict:
            if product_date >= start_date and product_date <= self.end_date:
                pending_products.append(dict[product_date])


def notify_to_scientific_processor(file_path):
    logging.debug("notify to scientific processor the processing of " + file_path)
    body = {"path": file_path}
    params = json.dumps(body).encode('utf8')
    req = urllib.request.Request("http://localhost:5002/process",
                                 data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)



def downloadProduct(product_name):
    new_product_path = config['DOWNLOADER']['inbox_path'] + product_name.replace("/", "-")[:-1]
    if not os.path.exists(new_product_path):
        os.makedirs(new_product_path)

    files_to_download=config['DOWNLOADER']['files_to_download'].split(',')
    for file_name in files_to_download:
        # TODO: move this key into config file
        url = "http://sentinel-s2-l1c.s3.amazonaws.com/" + product_name + file_name
        new_file_path = new_product_path + '/' +file_name
        urllib.request.urlretrieve(url, new_file_path)
        logging.debug("DOWNLOADED FILE WITH PATH ********>>>>> " + new_file_path)
    ps = ProductsService()
    ps.update_product_status(product_name, ProductStatus.downloaded)
    return

def process_product(product_name):
    product_path = config['DOWNLOADER']['inbox_path'] + product_name.replace("/", "-")[:-1]
    notify_to_scientific_processor(product_path + '/')
    return

def start_downloader():
    logging.debug("DOWNLOADER: START")
    logging.debug("(Downloader): read configurations")
    ps = ProductsService()

    # # GENERATE PRODUCT LIST
    # threads = []
    # for tile in config['FILTER']['tiles'].split(','):
    #     task = GenerateProductsList(tile,
    #                                 config['FILTER']['start_date'],
    #                                 config['FILTER']['end_date'])
    #     threads.append(task)
    #     task.start()
    #
    # # WAIT ALL THREADS
    # for thread in threads:
    #     thread.join()
    #
    # logging.debug("===== pending products =====")
    # for pending_product in pending_products:
    #
    #     ps.add_new_product(Product(name=str(pending_product),
    #                                status=ProductStatus.pending))
    #
    # logging.debug("XXXXXXXXXXXXXX++++++XXXXXXXXXXXXXXXXXOOOOOOO00000000000")
    #
    # # DOWNLOAD PRODUCTS
    # for product in ps.get_pending_products():
    #     logging.debug("+++++++++++++++++++++++++++")
    #     logging.debug(product.name)
    #     downloadProduct(product.name)

    # PROCESS PRODUCTS
    for product in ps.get_products_to_process():
        logging.debug("^^^^^^^^ PROCESS ^^^^^^^")
        logging.debug("send message to process: " + product.name)
        process_product(product.name)





if __name__ == '__main__':
    start()



