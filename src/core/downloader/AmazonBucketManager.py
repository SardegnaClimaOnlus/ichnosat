#!/usr/bin/env python

# ==================================================================================== #
#  __     ______     __  __     __   __     ______     ______     ______     ______
# /\ \   /\  ___\   /\ \_\ \   /\ "-.\ \   /\  __ \   /\  ___\   /\  __ \   /\__  _\
# \ \ \  \ \ \____  \ \  __ \  \ \ \-.  \  \ \ \/\ \  \ \___  \  \ \  __ \  \/_/\ \/
#  \ \_\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\  \ \_\ \_\    \ \_\
#   \/_/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/   \/_/\/_/     \/_/
#
# ==================================================================================== #
#
# Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #


import datetime
import re
from collections import OrderedDict
import urllib.request
import xml.etree.ElementTree as ET
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


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

    def load_products(self, tile, year, paginated=False):
        logger.debug("(AmazonBucketManager load_products)")
        # Generate url for year
        url = self.generate_url(tile, year)
        # Append to url start_from attribute if the request is paginated
        if paginated:
            url = url + "&start-after=" + self.last_item
        # Http request
        response = urllib.request.urlopen(url)
        root = ET.fromstring(response.read().decode('utf-8'))
        # Extract data from xml
        contents = root.findall('{'+self.config.aws_xmlns+'}Contents')
        for item in contents:
            key = item.find('{' + self.config.aws_xmlns + '}Key').text
            product_path = ''
            try:
                product_path = re.search(self.config.aws_products_regex, key)
            except ValueError:
                logger.warn("Product not found for key: " + key)
            self.product_list.append(product_path.group(0))
        # Check if the page is truncated (paginated case)
        if root.find('{' + self.config.aws_xmlns + '}IsTruncated').text == 'true':
            self.last_item = contents[-1].find('{' + self.config.aws_xmlns + '}Key').text
            return True
        else:
            return False

    def get_products_list(self, searchFilter):
        logger.debug("(AmazonBucketManager get_products_list)")
        tile = searchFilter.tile
        self.product_list = []
        self.last_item = None
        year = int(searchFilter.start_date.year)
        current_year = datetime.datetime.now().year
        pending_products = []
        # Extract whole list of products via amazon, from start year to now
        while year <= current_year:
            is_truncated = self.load_products(tile, year, False)
            while is_truncated:
                is_truncated = self.load_products(tile, year, True)
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
            if product_date >= searchFilter.start_date and product_date <= searchFilter.end_date:
                pending_products.append(dict[product_date])
        return pending_products

