from flask import Flask
app = Flask(__name__)
import pika
import subprocess
import json

@app.route('/')
def hello_world():
    return 'Hello from flask'

@app.route('/notify-scientific-processor')
def notify_scientific_processor():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    body_obj = {"source": "/usr/ichnosat/pre-processor/outbox/01/",
                "destination": "/usr/ichnosat/scientific-processor/outbox/01/"}
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=json.dumps(body_obj))
    print(" [x] Sent 'Hello World!'")
    connection.close()
    return "done"

@app.route('/start-scientific-processor')
def start_scientific_processor():
    subprocess.Popen(["/bin/bash", "bash/start-scientific-processor.sh", "var=11; ignore all"])
    return "done"

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


if __name__ == '__main__':
    subprocess.Popen(["/bin/bash", "bash/start-rabbitmq.sh", "var=11; ignore all"])
    app.run(debug=True,host='0.0.0.0')