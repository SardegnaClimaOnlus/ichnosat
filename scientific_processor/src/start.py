# !/usr/bin/env python
import pika
import logger
import logging
from ctypes import *
import json
import shutil
import fnmatch
import re
import os, sys, select
from flask import Flask, request
app = Flask(__name__)
from flask_cors import CORS, cross_origin
from scientific_processor.src.logger import *
from scientific_processor.src.ScientificProcessor import ScientificProcessor
CORS(app)



def process(source):
    logging.debug("process method")
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
                logging.debug("FOUND")
                product_name = source.split('/')[-2]
                logging.debug("product_name")
                logging.debug(product_name)

                logging.debug("source")
                logging.debug(source)
                plugin_path = os.path.join(dName, fileName)
                regex_plugin_name = re.escape(dName ) + '\/(.*?)\.so'
                plugin_name = re.match(regex_plugin_name, plugin_path).group(1)

                destination = outbox_path + product_name + "-" + plugin_name + '/'
                # create new product
                if not os.path.exists(destination):
                    os.makedirs(destination)
                logging.debug(destination)

                logging.debug("START Plugin: " + plugin_path)
                logging.debug('start processing')
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

    # remove file
    #shutil.rmtree(source)




@app.route('/process', methods=['POST'])
def process_req():
    logging.debug("><><><><><><><><><>--->  /process ")
    logging.debug("||||||||||||||| OOOOOO OOOO0000OOO0O0O0O0||||| ><><><><><><><><><>--->  request.get_json() ::::")
    obj = request.get_json()
    logging.debug("obj['path']--------------------------------------")
    logging.debug(obj['path'])
    app.scientific_processor.push_product(obj['path'])
    return obj['path']


def main():
    logging.debug("><><><><><><><><><>--->  scientific-processor")
    #app.queue = []
    logging.debug("main()")
    logging.debug(">>>> create a new scientific_processor")
    app.scientific_processor = ScientificProcessor()
    logging.debug(">>>> created new scientific_processor")
    logging.debug(app.scientific_processor)
    app.run(debug=True, host='0.0.0.0', port=5002)

    return


def start_scientific_processor():
    logging.debug("HELLO FROM SCIENTIFIC-PROCESSOR MAIN")
    main()

if __name__ == '__main__':
    main()