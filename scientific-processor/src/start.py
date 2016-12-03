# !/usr/bin/env python
import pika
from logger import logger
from ctypes import *
import json
import shutil
import os, fnmatch
import re

from  ScientificProcessor import ScientificProcessor

def process(source):
    logger.debug("process method")
    logger.debug(source)
    inDIR = '/usr/ichnosat/scientific-processor/src/plugins/'
    outbox_path = '/usr/ichnosat/scientific-processor/outbox/'
    pattern = '*.so'
    fileList = []
    logger.debug("before for")
    for dName, sdName, fList in os.walk(inDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):  # Match search string
                logger.debug("FOUND")
                product_name = source.split('/')[-2]
                logger.debug("product_name")
                logger.debug(product_name)

                logger.debug("source")
                logger.debug(source)
                plugin_path = os.path.join(dName, fileName)
                regex_plugin_name = re.escape(dName )+ '\/(.*?)\.so'
                plugin_name= re.match(regex_plugin_name, plugin_path).group(1)

                destination = outbox_path + product_name + "-" + plugin_name + '/'
                #create new product
                if not os.path.exists(destination):
                    os.makedirs(destination)
                logger.debug(destination)


                logger.debug("START Plugin: " + plugin_path)
                logger.debug('start processing')
                cdll.LoadLibrary(plugin_path)
                libc = CDLL(plugin_path)
                productPath = source.encode('utf-8')
                destinationPath = destination.encode('utf-8')
                libc.process.argtypes = [c_char_p]
                libc.process(productPath, destinationPath)
                logger.debug("FINISHED Plugin: " + plugin_path)

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


        logger.debug('start processing of new product')
        #p = subprocess.Popen(["/bin/bash", "test.sh", "var=11; ignore all"])
        if(os.path.isdir(data["source"])):
            process(data["source"])
            logger.debug('COMPLETED processing for the product with path: ' + data['source'])
        else:
            logger.debug("product not found - " + data["source"])
        #logger.debug('completed processing of new product')

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)


    print(' scientific-processor::: To exit press CTRL+C')
    #channel.start_consuming()
    logger.debug('STARTED SCIENTIFIC-PROCESSOR!!!!')


    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()




if __name__ == '__main__':
    main()