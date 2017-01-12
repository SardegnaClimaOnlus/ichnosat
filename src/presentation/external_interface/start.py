from flask import Flask
from flask_cors import CORS
from src.data.logger.logger import logger

app = Flask(__name__)
CORS(app)


from src.core.system_manager.system_manager import SystemManager

@app.route('/compile-plugins')
def compile_plugins():
  app.system_manager.compile_plugins()
  return "done"

@app.route('/start-downloader')
def start_downloader_interface():
    app.system_manager.trigger_downloader()
    return "done"

@app.route('/database', methods=['GET','POST'])
def create_database():
    app.system_manager.create_database()
    return "done"

if __name__ == '__main__':
    app.system_manager = SystemManager()
    app.run(debug=True, host='0.0.0.0', port=5000)
