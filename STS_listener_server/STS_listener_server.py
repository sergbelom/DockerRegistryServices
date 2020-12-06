#!/usr/bin/env python3

import os
import json
import logging
from flask import Flask, request

app = Flask(__name__)

LOG_FILE = os.path.join('listener_log', 'log.log')
logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('LOG STARTED')

@app.route('/log/', methods=['GET'])
def get_value(key):
    logging.info(str(key))
    return '', 200

@app.route('/log/', methods=['PUT'])
def add_value(key):
    logging.info(str(key))
    return '', 200

@app.route('/log/', methods=['POST'])
def show_post(key):
    logging.info(str(key))
    return '', 200

@app.route('/log/', methods=['DELETE'])
def delete_value(key):
    logging.info(str(key))
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
