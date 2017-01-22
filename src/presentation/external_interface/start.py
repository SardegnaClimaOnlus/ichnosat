from flask import Flask
from flask_cors import CORS
from src.data.logger.logger import logger
import json
import sys

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

@app.route('/create-database', methods=['GET','POST'])
def create_database():
    logger.debug("(Presentation create_database)  >>>>>>>>>> ")
    outcome = app.system_manager.create_database()
    logger.debug("(Presentation create_database)  outcome: " + str(outcome))
    if outcome:
        logger.debug("(Presentation create_database)  >>>>>> set first installation config !!!! " )
        success = app.system_manager.set_first_installation_config(False)
        if success :
            return "done"
        else:
            return "error", 500
    else:
        logger.debug("(Presentation create_database)  >>>>>> RETURN A 500")
        return "error", 500



# -- PRODUCTS -- #
@app.route('/products/pending')
def get_pending_products():
    logger.debug("(Presentation get_pending_products) ")
    response = ""

    try:
        response = str(app.system_manager.get_pending_products())
    except Exception as inst:
        logger.debug("(Presentation get_pending_products) Unexpected error:" )
        logger.debug(inst)

    return response


@app.route('/products/downloading')
def get_downloading_products():
    return str(app.system_manager.get_downloading_products())

@app.route('/products/downloaded')
def get_downloaded_products():
    return str(app.system_manager.get_downloaded_products())

@app.route('/products/processing')
def get_processing_products():
    return str(app.system_manager.get_processing_products())

@app.route('/products/processed')
def get_processed_products():
    return str(app.system_manager.get_processed_products())

@app.route('/first-installation')
def is_first_installation():
    is_first_installation = app.system_manager.is_first_installation()
    value = 'true' if  is_first_installation else 'false'
    return "{ \"first_installation\": \"" + value + "\"}"



if __name__ == '__main__':
    app.system_manager = SystemManager()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)







