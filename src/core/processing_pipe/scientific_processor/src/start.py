from flask import Flask, request
from src.core.processing_pipe.src.JobDispatcher import JobDispatcher
from src.data.logger.logger import logger
from flask_cors import CORS
import configparser

app = Flask(__name__)
CORS(app)

config_file_path = "/usr/ichnosat/src/core/processing_pipe/scientific_processor/src/config/config.cfg"


@app.route('/process', methods=['POST'])
def process_req():
    app.job_dispatcher.publish_new_job(request.get_json()['path'])
    return "done"

def main():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    app.job_dispatcher = JobDispatcher(config['PATHS']['outbox_path'], config['PATHS']['plugins_path'])
    app.run(debug=True, host=config['SERVER']['host'], port=int(config['SERVER']['port']))

    return

2
if __name__ == '__main__':
    main()

