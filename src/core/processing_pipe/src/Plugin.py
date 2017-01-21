from src.data.logger.logger import logger
import os, sys, select
from ctypes import *
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import ProductStatus

class Plugin():
    def __init__(self, plugin_name, plugin_path):
        self.productService = ProductsService()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path
        sys.stdout.write(' \b')
        self.pipe_out, pipe_in = os.pipe()
        self.stdout = os.dup(1)
        os.dup2(pipe_in, 1)
        return

    def more_data(self):
        r, _, _ = select.select([self.pipe_out], [], [], 0)
        return bool(r)

    def read_pipe(self):
        while self.more_data():
            logger.debug(os.read(self.pipe_out, 1024).decode('utf-8'))

    def run(self, source, outbox_path):
        try:

            product_name = source.split('/')[-2]
            self.productService.update_product_status(product_name, ProductStatus.processing)
            destination = outbox_path + product_name + "-" + self.plugin_name + '/'
            if not os.path.exists(destination):
                os.makedirs(destination)
            cdll.LoadLibrary(self.plugin_path)
            libc = CDLL(self.plugin_path)
            productPath = source.encode('utf-8')
            destinationPath = destination.encode('utf-8')
            libc.process.argtypes = [c_char_p]
            libc.process(productPath, destinationPath)
            self.productService.update_product_status(product_name, ProductStatus.processed)
            os.dup2(self.stdout, 1)
            self.read_pipe()
        except ValueError:
            logger.warn("Failed scientific-processor plugin with name: " + self.plugin_name)