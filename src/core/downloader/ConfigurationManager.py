from src.core.downloader.Configuration import Configuration
import re
import datetime
import configparser
from src.data.logger.logger import logger

class ConfigurationManager:
    def __init__(self):
        logger.debug("(ConfigurationManager __init__)")
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/downloader/config/config.cfg")
        self.configuration = Configuration()
        self.load_configuration()

    def get_configuration(self):
        return self.configuration

    def datetime_from_string(self, date_string):
        date_regex = "([0-9]*)/([0-9]*)/([0-9]*)"
        date_match = re.search(date_regex, date_string)
        return datetime.date(int(date_match.group(1)),
                             int(date_match.group(2)),
                             int(date_match.group(3)))
    def load_end_date(self ):
        end_date = self.config['FILTER']['end_date']
        if end_date != 'NOW':
            return self.datetime_from_string(end_date)
        else:
            return datetime.datetime.now().date()

    def load_start_date(self):
        start_date = self.config['FILTER']['start_date']
        return self.datetime_from_string(start_date)

    def load_tiles(self):
        return self.config['FILTER']['tiles'].split(',')

    def load_files_to_download(self):
        return self.config['FILTER']['files_to_download'].split(',')

    def load_aws_xmlns(self):
        return  self.config['AWS']['xmlns']

    def load_aws_products_regex(self):
        return self.config['AWS']['products_regex']

    def load_aws_domain(self):
        return self.config['AWS']['domain']

    def load_inbox_path(self):
        return self.config['DOWNLOADER']['inbox_path']

    def load_configuration(self):
        logger.debug("(ConfigurationManager load_configuration)")
        self.configuration.start_date = self.load_start_date()
        self.configuration.end_date = self.load_end_date()
        self.configuration.tiles = self.load_tiles()
        self.configuration.files = self.load_files_to_download()
        self.configuration.aws_xmlns = self.load_aws_xmlns()
        self.configuration.aws_products_regex = self.load_aws_products_regex()
        self.configuration.aws_domain = self.load_aws_domain()
        self.configuration.inbox_path = self.load_inbox_path()
        logger.debug("(ConfigurationManager load_configuration) finished")











