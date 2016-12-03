# !/usr/bin/env python
import pika
from logger import logger
from ctypes import *
import json
import shutil
import os, fnmatch

from  ScientificProcessor import ScientificProcessor

def process(source, destination):
    logger.debug("process method")
    logger.debug(source)
    logger.debug(destination)
    logger.debug("iglob")

    inDIR = '/usr/ichnosat/scientific-processor/src/plugins/'
    pattern = '*.so'
    fileList = []

    # Walk through directory
    for dName, sdName, fList in os.walk(inDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):  # Match search string
                path =os.path.join(dName, fileName)
                logger.debug("START Plugin: " + path)
                logger.debug('start processing')
                cdll.LoadLibrary(path)
                libc = CDLL(path)
                productPath = source.encode('utf-8')
                destinationPath = destination.encode('utf-8')
                libc.process.argtypes = [c_char_p]
                libc.process(productPath, destinationPath)
                print("DONE")

    shutil.rmtree(source)

    #remove file


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
        process(data["source"], data["destination"])
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