from src.core.downloader.Configuration import Configuration
import re
import datetime
import configparser

class ConfigurationManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("/usr/ichnosat/src/core/downloader/config/config.cfg")
        self.configuration = Configuration()
        self.load_configuration()

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

    def load_aws_config(self):
        aws = {}
        aws.xmlns = self.config['AWS']['xmlns']
        aws.products_regex = self.config['AWS']['products_regex']
        aws.domain = self.config['AWS']['domain']
        return aws

    def load_inbox_path(self):
        return self.config['DOWNLOADER']['inbox_path']

    def load_configuration(self):
        self.configuration.start_date = self.load_start_date()
        self.configuration.end_date = self.load_end_date()
        self.configuration.tiles = self.load_tiles()
        self.configuration.files = self.load_files_to_download()
        self.configuration.aws = self.load_aws_config()
        self.configuration.inbox_path = self.load_inbox_path()











