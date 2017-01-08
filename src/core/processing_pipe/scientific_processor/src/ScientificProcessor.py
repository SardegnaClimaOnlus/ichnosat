
from time import sleep
import threading
from src.data.logger.logger import logger
import os, sys, select
from ctypes import *
import fnmatch
import re

class ScientificProcessor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        logger.debug('Created new ScientificProcessor')
        self.queue = []
        self.processing = False
        self.lock = threading.Lock()

    def push_product(self, product):
        logger.debug("scientific processor JJJJJJJJJ")
        logger.debug("before self.queue lenght")
        logger.debug(len(self.queue))
        self.queue.append(product)
        logger.debug("after self.queue lenght")
        logger.debug(len(self.queue))
        self.process()

    def process_product(self, source):
        logger.debug("XXXXXXXXXXXXXXXXX  process method")
        logger.debug(source)
        # TODO: create a configuration file for this hardcoded string
        inDIR = '/usr/ichnosat/src/core/processing_pipe/scientific_processor/src/plugins/'
        outbox_path = '/usr/ichnosat/data_local/outbox/'
        pattern = '*.so'
        fileList = []
        logger.debug("before for ------))")

        sys.stdout.write(' \b')
        pipe_out, pipe_in = os.pipe()
        stdout = os.dup(1)
        os.dup2(pipe_in, 1)

        # check if we have more to read from the pipe
        def more_data():
            r, _, _ = select.select([pipe_out], [], [], 0)
            return bool(r)

        # read the whole pipe
        def read_pipe():
            out = ''
            while more_data():
                logger.debug(os.read(pipe_out, 1024).decode('utf-8'))

        for dName, sdName, fList in os.walk(inDIR):
            for fileName in fList:
                if fnmatch.fnmatch(fileName, pattern):  # Match search string
                    try:
                        logger.debug("FOUND")
                        product_name = source.split('/')[-2]
                        logger.debug("product_name")
                        logger.debug(product_name)

                        logger.debug("source")
                        logger.debug(source)
                        plugin_path = os.path.join(dName, fileName)
                        regex_plugin_name = re.escape(dName) + '\/(.*?)\.so'
                        plugin_name = re.match(regex_plugin_name, plugin_path).group(1)

                        destination = outbox_path + product_name + "-" + plugin_name + '/'
                        # create new product
                        if not os.path.exists(destination):
                            os.makedirs(destination)
                        logger.debug(destination)

                        logger.debug("START Plugin: " + plugin_path)
                        logger.debug('start processing')
                        logger.debug("------ plugin_path")
                        logger.debug(plugin_path)
                        cdll.LoadLibrary(plugin_path)
                        libc = CDLL(plugin_path)
                        productPath = source.encode('utf-8')
                        destinationPath = destination.encode('utf-8')
                        libc.process.argtypes = [c_char_p]
                        libc.process(productPath, destinationPath)
                        # put stdout back in place
                        os.dup2(stdout, 1)
                        logger.debug('Contents of our stdout pipe:')
                        read_pipe()
                        logger.debug("FINISHED Plugin: " + plugin_path)
                    except ValueError:
                        logger.debug("Failed scientific-processor plugin with name: " + plugin_name)


                    # remove file
                    # shutil.rmtree(source)

    def process(self):
        logger.debug("HHHHHHHHHHH PROCESS")
        logger.debug("self.processing")
        logger.debug(self.processing)
        self.lock.acquire()
        if self.processing:
            self.lock.release()
            return
        self.processing = True
        self.lock.release()
        logger.debug("KKKKK after check")
        logger.debug("self.processing")
        logger.debug(self.processing)
        logger.debug("len(self.queue ) KKKKKKKK")
        logger.debug(len(self.queue ))
        while len(self.queue ) > 0:


            # get a product from queue
            product = self.queue.pop()
            # process product
            logger.debug("88888888 --) product: " + product)
            self.process_product(product)

        self.lock.acquire()

        self.processing = False
        self.lock.release()

        return





