#!/usr/bin/env python

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class SearchFilter:
    def __init__(self,tile, start_date, end_date):
        self.tile = tile
        self.start_date = start_date
        self.end_date = end_date
        return