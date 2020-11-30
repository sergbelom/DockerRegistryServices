#!/usr/bin/env python3
import json
from flask import Flask, request
app = Flask(__name__)
REGISTRY = {}

@app.route('/registry/', methods=['GET'])
def get_value(key):
    print(str(key))
    return '', 200

@app.route('/registry/', methods=['PUT'])
def add_value(key):
    print(str(key))
    return '', 200

@app.route('/registry/', methods=['POST'])
def show_post(key):
    print(str(key))
    return '', 200

@app.route('/registry/', methods=['DELETE'])
def delete_value(key):
    print(str(key))
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
