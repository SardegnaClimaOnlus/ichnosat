
from time import sleep
import threading
from src.data.logger.logger import *
import logging
import os, sys, select
from ctypes import *
import fnmatch
import re

class ScientificProcessor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        logging.debug('Created new ScientificProcessor')
        self.queue = []
        self.processing = False
        self.lock = threading.Lock()

    def push_product(self, product):
        logging.debug("scientific processor JJJJJJJJJ")
        logging.debug("before self.queue lenght")
        logging.debug(len(self.queue))
        self.queue.append(product)
        logging.debug("after self.queue lenght")
        logging.debug(len(self.queue))
        self.process()

    def process_product(self, source):
        logging.debug("XXXXXXXXXXXXXXXXX  process method")
        logging.debug(source)
        inDIR = '/usr/ichnosat/scientific_processor/src/plugins/'
        outbox_path = '/usr/ichnosat/scientific_processor/outbox/'
        pattern = '*.so'
        fileList = []
        logging.debug("before for")

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
                logging.debug(os.read(pipe_out, 1024).decode('utf-8'))

        for dName, sdName, fList in os.walk(inDIR):
            for fileName in fList:
                if fnmatch.fnmatch(fileName, pattern):  # Match search string
                    try:
                        logging.debug("FOUND")
                        product_name = source.split('/')[-2]
                        logging.debug("product_name")
                        logging.debug(product_name)

                        logging.debug("source")
                        logging.debug(source)
                        plugin_path = os.path.join(dName, fileName)
                        regex_plugin_name = re.escape(dName) + '\/(.*?)\.so'
                        plugin_name = re.match(regex_plugin_name, plugin_path).group(1)

                        destination = outbox_path + product_name + "-" + plugin_name + '/'
                        # create new product
                        if not os.path.exists(destination):
                            os.makedirs(destination)
                        logging.debug(destination)

                        logging.debug("START Plugin: " + plugin_path)
                        logging.debug('start processing')
                        logging.debug("------ plugin_path")
                        logging.debug(plugin_path)
                        cdll.LoadLibrary(plugin_path)
                        libc = CDLL(plugin_path)
                        productPath = source.encode('utf-8')
                        destinationPath = destination.encode('utf-8')
                        libc.process.argtypes = [c_char_p]
                        libc.process(productPath, destinationPath)
                        # put stdout back in place
                        os.dup2(stdout, 1)
                        logging.debug('Contents of our stdout pipe:')
                        read_pipe()
                        logging.debug("FINISHED Plugin: " + plugin_path)
                    except ValueError:
                        logging.debug("Failed scientific-processor plugin with name: " + plugin_name)


                    # remove file
                    # shutil.rmtree(source)

    def process(self):
        logging.debug("HHHHHHHHHHH PROCESS")
        logging.debug("self.processing")
        logging.debug(self.processing)
        self.lock.acquire()
        if self.processing:
            self.lock.release()
            return
        self.processing = True
        self.lock.release()
        logging.debug("KKKKK after check")
        logging.debug("self.processing")
        logging.debug(self.processing)
        logging.debug("len(self.queue ) KKKKKKKK")
        logging.debug(len(self.queue ))
        while len(self.queue ) > 0:


            # get a product from queue
            product = self.queue.pop()
            # process product
            logging.debug("88888888 --) product: " + product)
            self.process_product(product)

        self.lock.acquire()

        self.processing = False
        self.lock.release()

        return





