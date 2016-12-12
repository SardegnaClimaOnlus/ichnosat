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


def extract_date(item):
    regex = 'tiles/[0-9]2/[A-Z]/[A-Z]{2}/([0-9]{4})/([0-9]*)/([0-9]*)/'
    match = re.search(regex, item)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    logging.debug('year: ' + year)
    logging.debug('month: ' + month)
    logging.debug('day: ' + day)
    return datetime.date(int(year), int(month), int(day))

class GenerateProductsList(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.product_list = []

    def load_products(self, paginated=False):
        url = ''
        if paginated:
            url = self.url + "&start-after=" + self.last_item
        else:
            url = self.url
        logging.debug(">>>>>>>> REQUEST <<<<<<<<<<")
        logging.debug(url)
        response = urllib.request.urlopen(url)
        data1 = response.read()
        root = ET.fromstring(data1.decode('utf-8'))
        contents = root.findall('{'+config['AWS']['xmlns']+'}Contents')
        for item in contents:

            key = item.find('{' + config['AWS']['xmlns'] + '}Key').text
            product_path = ''
            try:
                product_path = re.search(config['AWS']['products_regex'], key)
            except ValueError:
                logging.error("error parsing")

            self.product_list.append(product_path.group(0))

        isTruncated = root.find('{' + config['AWS']['xmlns'] + '}IsTruncated').text

        if isTruncated == 'true':
            self.last_item = contents[-1].find('{' + config['AWS']['xmlns'] + '}Key').text
            return True
        else:
            return False


    def run(self):
        logging.debug("(Downloader DownloadTask run)  url:" + self.url);
        # get the products list

        isTruncated = self.load_products()
        while isTruncated:
            time.sleep(2)
            isTruncated = self.load_products(True)

        # get IsTruncated
        logging.debug("----- products_list -----")
        self.product_list = set(self.product_list)
        dict = {}
        for product in self.product_list:
            date = extract_date(str(product))
            product_string = str(product)
            logging.debug(date)
            dict[date] = product_string
            logging.debug(product_string)

        logging.debug("===== print dictionary =====")


        dict = OrderedDict(sorted(dict.items()))
        for x in dict:
            logging.debug(str(x) + ':' + str(dict[x]))






def generate_urls(url_template, tiles, start_year, start_month):
    urls = []
    for tile in tiles:
        url =url_template.format(tile=tile, year=start_year, month=start_month)
        logging.debug('url: '+ url)
        urls.append(url)
    logging.debug("(Downloader, generate_urls) END")
    return urls

def start():
    logging.debug("DOWNLOADER: START")
    logging.debug("(Downloader): read configurations")
    start_month = config['FILTER']['start_month']
    start_year  = config['FILTER']['start_year']
    url_template = config['FILTER']['url_template']
    tiles = config['FILTER']['tiles'].split(',')
    urls = generate_urls(url_template, tiles, start_year, start_month)
    # generate products list
    for url in urls:
        download_task = GenerateProductsList(url)
        download_task.run()








if __name__ == '__main__':
    start()



