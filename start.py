from flask import Flask
app = Flask(__name__)
import pika
import subprocess
import json
import logging
import logger
import os
import downloader.start




@app.route('/')
def hello_world():

    return 'Hello from flask'



@app.route('/notify-scientific-processor')
def notify_scientific_processor():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    body_obj = {"source": "/usr/ichnosat/pre-processor/outbox/10SDG20151207_0/"}
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=json.dumps(body_obj))
    print(" [x] Sent 'Hello World!'")
    connection.close()
    return "done"

@app.route('/start-scientific-processor')
def start_scientific_processor():
    logging.debug("[ichnosat-manager][]: Start scientific-processor")
    subprocess.Popen(["/bin/bash", "bash/start-scientific-processor.sh", "var=11; ignore all"])
    return "done"

@app.route('/compile-plugins')
def compile_plugins():
    logging.debug("(ichnosat-manager): START compile scientific-processor plugins")
    dirnames = os.listdir('/usr/ichnosat/scientific-processor/src/plugins/')
    r = re.compile('^[^\.]')
    dirnames = filter(r.match, dirnames)

    for plugin_name in dirnames:
        try:
            completed_without_error = True
            logging.debug("(ichnosat-manager): START compile of scientific-plugin '" + plugin_name + "' plugin")
            p = subprocess.Popen(["/bin/bash", "bash/compile-plugins.sh", plugin_name, "var=11; ignore all"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            for line in p.stdout.read().decode('utf-8').split("\n"):
                if (len(line) > 0):
                    logging.debug("(BASH - compile-plugins.sh): " + line)

            for line in p.stderr.read().decode('utf-8').split("\n"):
                if (len(line) > 0):
                    logging.debug("[ERROR] (BASH compile-plugins.sh): " + line)
                    completed_without_error = False

            if(completed_without_error):
                logging.debug("(ichnosat-manager): Completed compile " + plugin_name + " plugin")
            else:
                logging.debug("[ERROR] (ichnosat-manager): Failed compilation of scientific-processor plugin '" + plugin_name + "'")

        except ValueError:
            logging.debug(
                "[ERROR] (ichnosat-manager): Failed compilation of scientific-processor plugin '" + plugin_name + "'")

    logging.debug("(ichnosat-manager): COMPLETED compile scientific-processor plugins")

    return "Done"

@app.route('/start-rabbitmq')
def start_rabbitmq():
    subprocess.Popen(["/bin/bash", "bash/start-rabbitmq.sh", "var=11; ignore all"])
    return "done"

@app.route('/stop-rabbitmq')
def stop_rabbitmq():
    subprocess.Popen(["/bin/bash", "bash/stop-rabbitmq.sh", "var=11; ignore all"])
    return "done"

@app.route('/rabbitmq-version')
def version_rabbitmq():
    subprocess.Popen(["/bin/bash", "bash/rabbitmq-version.sh", "var=11; ignore all"])
    return "done"


@app.route('/network-test')
def network_test():
    subprocess.Popen(["/bin/bash", "bash/network-test.sh", "var=11; ignore all"])
    return "done"

@app.route('/start-downloader')
def start_downloader():
    logging.debug("start-downloder")
    downloader.start.start()
    return "started-download"


if __name__ == '__main__':
    subprocess.Popen(["/bin/bash", "bash/start-rabbitmq.sh", "var=11; ignore all"])
    app.run(debug=True,host='0.0.0.0')