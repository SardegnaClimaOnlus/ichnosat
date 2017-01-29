#!/usr/bin/env python

from flask import Flask, request
from src.data.database.db import DB
from src.core.processing_pipe.src.JobDispatcher import JobDispatcher
from src.data.logger.logger import logger
from flask_cors import CORS
import configparser

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Sardegna Clima"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


app = Flask(__name__)
CORS(app)

config_file_path = "/usr/ichnosat/src/core/processing_pipe/scientific_processor/src/config/config.cfg"


@app.route('/process', methods=['POST'])
def process_req():
    logger.debug("(scientific_processor.start.py process_req) ")
    try:
        app.job_dispatcher.publish_new_job(request.get_json()['path'])
    except Exception as inst:
        logger.debug("(scientific_processor.start.py process_req)  Unexpected error:" )
        logger.debug(inst)
    return "done"

def main():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    app.job_dispatcher = JobDispatcher(config['PATHS']['outbox_path'], config['PATHS']['plugins_path'])
    app.run(debug=True, host=config['SERVER']['host'], port=int(config['SERVER']['port']), threaded=True)

    return

2
if __name__ == '__main__':
    main()

