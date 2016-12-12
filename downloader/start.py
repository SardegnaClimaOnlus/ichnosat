import logging
import configparser
import threading
import urllib.request
import xml.etree.ElementTree as ET
import re
import time
import datetime
from collections import OrderedDict



config = configparser.ConfigParser()
config.read("downloader/config/config.cfg")

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
    def __init__(self, tile, start_year, start_month, start_day):
        self.tile = tile
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.product_list = []
        self.last_item = None
        self.current_year = datetime.datetime.now().year
        logging.debug("CURRENT YEAR: " + str(self.current_year))

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

        # PRINT DICTIONARY
        logging.debug("===== print dictionary =====")
        for x in dict:
            logging.debug(str(x) + ':' + str(dict[x]))

        # TODO: FILTER IN DATE INTERVAL




def start():
    logging.debug("DOWNLOADER: START")
    logging.debug("(Downloader): read configurations")

    # generate products list
    for tile in config['FILTER']['tiles'].split(','):
        download_task = GenerateProductsList(tile,
                                             config['FILTER']['start_year'],
                                             config['FILTER']['start_month'],
                                             config['FILTER']['start_day'])
        download_task.run()








if __name__ == '__main__':
    start()



