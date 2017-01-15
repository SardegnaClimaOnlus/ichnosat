from src.core.downloader.AmazonBucketManager import AmazonBucketManager
from src.core.downloader.ProductDownloader import ProductDownloader

class Datasource:
    def __init__(self, configurations):
        self.configurations = configurations
        self.abm = AmazonBucketManager(self.configurations)
        self.productDownloader = ProductDownloader(self.configuration.inbox_path,
                                                   self.configuration.files_to_download,
                                                   self.configuration.aws.domain)
        return

    def get_products_list(self, searchFilter):
        return self.abm.get_products_list(searchFilter)

    def download_product(self,product):
        self.productDownloader.download_product(product)
