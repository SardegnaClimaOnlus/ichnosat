# !/usr/bin/env python
import pika
import logging
from ctypes import *
import json
import shutil
import fnmatch
import re
import os, sys, select

from  ScientificProcessor import ScientificProcessor

def process(source):
    logging.debug("process method")
    logging.debug(source)
    inDIR = '/usr/ichnosat/scientific-processor/src/plugins/'
    outbox_path = '/usr/ichnosat/scientific-processor/outbox/'
    pattern = '*.so'
    fileList = []
    logging.debug("before for")
    ############-------------
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



    ###########-------------
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
                regex_plugin_name = re.escape(dName )+ '\/(.*?)\.so'
                plugin_name= re.match(regex_plugin_name, plugin_path).group(1)

                destination = outbox_path + product_name + "-" + plugin_name + '/'
                #create new product
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




def main():
   # scientificProcessor = ScientificProcessor()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', heartbeat_interval=200))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        #source = "/usr/ichnosat/scientific-processor/inbox/01/"
        #destination = "/usr/ichnosat/scientific-processor/outbox/01/"
        #print(" [x] Received %r" % body)
        data = json.loads(body.decode("utf-8") )


        logging.debug('start processing of new product')
        #p = subprocess.Popen(["/bin/bash", "test.sh", "var=11; ignore all"])
        if(os.path.isdir(data["source"])):
            process(data["source"])
            logging.debug('COMPLETED processing for the product with path: ' + data['source'])
        else:
            logging.debug("product not found - " + data["source"])
        #logging.debug('completed processing of new product')

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)


    print(' scientific-processor::: To exit press CTRL+C')
    #channel.start_consuming()
    logging.debug('STARTED SCIENTIFIC-PROCESSOR!!!!')


    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()




if __name__ == '__main__':
    main()