from flask import Flask
app = Flask(__name__)
from flask_cors import CORS

from src.data.logger.logger import logger


from src.core.processing_pipe.src.PluginManager import PluginManager
from src.core.downloader.start import start_downloader
from src.data.database.db import DB
CORS(app)


@app.route('/compile-plugins')
def compile_plugins():
  pm = PluginManager()
  pm.compile_plugins()
  return "done"

@app.route('/start-downloader')
def start_downloader_interface():
    logger.debug("start downloader")
    start_downloader()
    return "done"

@app.route('/database', methods=['GET','POST'])
def create_database():
    db = DB()
    db.create_db()
    return "done"

if __name__ == '__main__':
    logger.debug("(external_interface) Start")
    app.run(debug=True, host='0.0.0.0', port=5000)
