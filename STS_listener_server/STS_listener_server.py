#!/usr/bin/env python3

import os
import json
import logging
from flask import Flask, request

app = Flask(__name__)

LOG_FILE = os.path.join('listener_log', 'log.log')
logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('LOG STARTED')

def print_dict_data(dict_data, prefix):
    for k, v in dict_data.items():
        if (type(v) == dict):
            logging.info(prefix + str(k) + ':')
            print_dict_data(v, prefix + '   ')
        else:
            logging.info(prefix + str(k) + ': ' + str(v))

def parse_and_log_request_data(data):
    json_data = json.loads(data)
    # logging.info(type(json_data))
    # logging.info(json_data['events'])
    events = json_data['events']
    event_count = 0
    for event in events:
        #logging.info(event_count)
        #event_count += 1
        if (type(event) == dict):
            print_dict_data(event,'')

@app.route('/log/', methods=['POST'])
def show_post():
    logging.info('!NEW ACTION NOTIFICATION!')
    logging.info('ARGUMENTS:')
    logging.info('count: ' + str(len(request.args)))
    for arg in request.args:
        logging.info(arg)
    logging.info('--------------------')
    logging.info('HEADERS:')
    logging.info('count: '+ str(len(request.headers)))
    for header in request.headers:
        logging.info(header)
    logging.info('--------------------')
    logging.info('DATA:')
    data = request.data.decode('utf-8')
    #logging.info(data)
    parse_and_log_request_data(data)
    logging.info('--------------------')
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
