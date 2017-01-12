from flask import Flask, request
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

from src.core.processing_pipe.src.JobDispatcher import JobDispatcher
from src.data.logger.logger import logger


@app.route('/process', methods=['POST'])
def process_req():
    app.job_dispatcher.publish_new_job(request.get_json()['path'])
    return "done"

def main():
    outbox_path = '/usr/ichnosat/data_local/outbox/'
    plugins_path = '/usr/ichnosat/src/core/processing_pipe/scientific_processor/src/plugins'
    app.job_dispatcher = JobDispatcher(outbox_path, plugins_path)
    app.run(debug=True, host='0.0.0.0', port=5002)

    return


if __name__ == '__main__':
    main()

