from flask import Flask

app = Flask(__name__)

import subprocess
import os
import z_old.downloader.start
from sqlalchemy import *
from sqlalchemy.orm import *
from z_old import database as db
from scientific_processor.src.start import *
from flask_cors import CORS

CORS(app)


@app.route('/compile-plugins')
def compile_plugins():
    logging.debug("(ichnosat-manager): START compile scientific_processor plugins")
    dirnames = os.listdir('/usr/ichnosat/scientific_processor/src/plugins/')
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
                logging.debug("[ERROR] (ichnosat-manager): Failed compilation of scientific_processor plugin '" + plugin_name + "'")

        except ValueError:
            logging.debug(
                "[ERROR] (ichnosat-manager): Failed compilation of scientific_processor plugin '" + plugin_name + "'")

    logging.debug("(ichnosat-manager): COMPLETED compile scientific_processor plugins")

    return "Done"



@app.route('/start-downloader')
def start_downloader():
    logging.debug("start-downloder")
    z_old.downloader.start.start()
    return "started-download"





@app.route('/database', methods=['GET','POST'])
def create_database():
    dd = db.DB()
    dd.create_db()
    return "Done"






if __name__ == '__main__':
    logging.debug("START ")
    logging.debug("START RABBITMQ")
    subprocess.Popen(["/bin/bash", "bash/init.sh", "var=11; ignore all"])


    app.run(debug=True,host='0.0.0.0')