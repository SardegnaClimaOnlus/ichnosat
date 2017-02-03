#!/usr/bin/env python

# ==================================================================================== #
#  __     ______     __  __     __   __     ______     ______     ______     ______
# /\ \   /\  ___\   /\ \_\ \   /\ "-.\ \   /\  __ \   /\  ___\   /\  __ \   /\__  _\
# \ \ \  \ \ \____  \ \  __ \  \ \ \-.  \  \ \ \/\ \  \ \___  \  \ \  __ \  \/_/\ \/
#  \ \_\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\  \ \_\ \_\    \ \_\
#   \/_/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/   \/_/\/_/     \/_/
#
# ==================================================================================== #
#
# Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #

from flask import Flask
from flask_cors import CORS
from src.core.system_manager.system_manager import SystemManager

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
    outcome = app.system_manager.create_database()
    if outcome:
        success = app.system_manager.set_first_installation_config(False)
        if success :
            return "done"
        else:
            return "error", 500
    else:
        return "error", 500

# -- PRODUCTS -- #
@app.route('/products/pending')
def get_pending_products():
    response = ""
    try:
        response = str(app.system_manager.get_pending_products())
    except Exception as inst:
        pass
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

@app.route('/database/fix')
def fix_inconsistent_data():
    app.system_manager.fix_inconsistent_data_in_db()
    return "done"

if __name__ == '__main__':
    app.system_manager = SystemManager()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
