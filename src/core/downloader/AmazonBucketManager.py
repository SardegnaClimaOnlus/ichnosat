import datetime
import re
from collections import OrderedDict
import urllib.request
import xml.etree.ElementTree as ET
from src.data.logger.logger import logger

class AmazonBucketManager:
    def __init__(self, configurations):
        self.config = configurations
        self.product_list = []
        self.last_item = None
        return

    def generate_url(self, tile, year):
        url_template = 'http://sentinel-s2-l1c.s3.amazonaws.com/?list-type=2&prefix=tiles/{tile}/{year}/'
        url = url_template.format(tile=tile, year=year)
        return url

    def extract_date(self, item):
        regex = 'tiles/[0-9]2/[A-Z]/[A-Z]{2}/([0-9]{4})/([0-9]*)/([0-9]*)/'
        match = re.search(regex, item)
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return datetime.date(int(year), int(month), int(day))

    def load_products(self, year, paginated=False):
        # Generate url for year
        url = self.generate_url(self.tile, year)
        # Append to url start_from attribute if the request is paginated
        if paginated:
            url = url + "&start-after=" + self.last_item
        # Http request
        response = urllib.request.urlopen(url)
        root = ET.fromstring(response.read().decode('utf-8'))
        # Extract data from xml
        contents = root.findall('{'+self.config.aws.xmlns+'}Contents')
        for item in contents:
            key = item.find('{' + self.config.aws.xmlns + '}Key').text
            product_path = ''
            try:
                product_path = re.search(self.config.aws.products_regex, key)
            except ValueError:
                logger.warn("Product not found for key: " + key)
            self.product_list.append(product_path.group(0))
        # Check if the page is truncated (paginated case)
        if root.find('{' + self.config.aws.xmlns + '}IsTruncated').text == 'true':
            self.last_item = contents[-1].find('{' + self.config.aws.xmlns + '}Key').text
            return True
        else:
            return False

    def get_products_list(self, searchFilter):
        self.product_list = []
        self.last_item = None
        year = int(searchFilter.start_date.year)
        current_year = datetime.datetime.now().year
        pending_products = []
        # Extract whole list of products via amazon, from start year to now
        while year <= current_year:
            is_truncated = self.load_products(year, False)
            while is_truncated:
                is_truncated = self.load_products(year, True)
            year += 1
        # Clean list of products
        self.product_list = set(self.product_list)
        # Generate dictionary
        dict = {}
        for product in self.product_list:
            date = self.extract_date(str(product))
            product_string = str(product)
            dict[date] = product_string
        # Sort dictionary
        dict = OrderedDict(sorted(dict.items()))
        # Filter products via date interval
        for product_date in dict:
            if product_date >= self.configuration.start_date and product_date <= self.configuration.end_date:
                pending_products.append(dict[product_date])
        return pending_products

