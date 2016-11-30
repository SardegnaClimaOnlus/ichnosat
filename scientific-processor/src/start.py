# !/usr/bin/env python
import pika
from logger import logger
import subprocess

from  ScientificProcessor import ScientificProcessor

def process():

    logger.debug('start processing')
    # get list of inbox folder
    # get the path of first folder in the list
    # generate list of .so files present in plugin folder
    # for each plugins:
    #     generate a folder in the outbox with name <product_folder_name>_<plugin_name>
    #     call the plugin passing the path of first folder in inbox and the path of the just created folder
    # remove the first folder in the list of inbox      
def main():
   # scientificProcessor = ScientificProcessor()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):

        print(" [x] Received %r" % body)
        logger.debug('start processing of new product')
        p = subprocess.Popen(["/bin/bash", "test.sh", "var=11; ignore all"])
        p.wait()

        logger.debug('completed processing of new product')

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