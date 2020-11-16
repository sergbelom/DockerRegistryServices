#!/usr/bin/env python

from flask import Flask, Response
from flask import (jsonify, request)

import re
import os
import sys
import json
import logging
import datetime
import argparse

import jwt
import base64
import hashlib
from Crypto.PublicKey import RSA

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format='%(asctime)s - %(message)s')
LOG = logging.getLogger(__name__)

CERT = os.path.join('..', 'certs', 'STS_docker_auth.crt')
KEY = os.path.join('..', 'certs', 'STS_docker_auth.key')
AUTH = os.path.join('users.auth')

SIGNKEY = None
AUTH_STORE = {}

app = Flask(__name__)

def response(status, data):
    """ Flask response """
    return Response(
        status=status,
        response=json.dumps(data, indent=2),
        mimetype='application/json')

def key_id_algorithm(priv_key_pem):
    pub_key_der = RSA.importKey(SIGNKEY).publickey().exportKey('DER')
    sha256 = hashlib.sha256(pub_key_der).digest()[:30]
    b32sha256 = base64.b32encode(sha256)
    buf = ""    
    for block_num in range(len(b32sha256) / 4):
        start = block_num * 4
        end = block_num * 4 + 4
        buf += b32sha256[start:end] + ":"
    return buf.rstrip(':')

# The key id based on algorithm from Dokcer:
# func keyIDFromCryptoKey(pubKey PublicKey) string {
# 	// Generate and return a 'libtrust' fingerprint of the public key.
# 	// For an RSA key this should be:
# 	//   SHA256(DER encoded ASN1)
# 	// Then truncated to 240 bits and encoded into 12 base32 groups like so:
# 	//   ABCD:EFGH:IJKL:MNOP:QRST:UVWX:YZ23:4567:ABCD:EFGH:IJKL:MNOP
# 	derBytes, err := x509.MarshalPKIXPublicKey(pubKey.CryptoPublicKey())
# 	if err != nil {
# 		return ""
# 	}
# 	hasher := crypto.SHA256.New()
# 	hasher.Write(derBytes)
# 	return keyIDEncode(hasher.Sum(nil)[:30])
# }

def get_allowed_actions(request_params):
    """Get list of allowed actions"""
    allowed_actions = []
    for requested_permissions in request_params['scope']:
            type, name, actions = requested_permissions.split(':')
            actions = actions.split(',')
            allowed_actions.append({
                'type': type,
                'name': name,
                'actions': actions
            })
    return allowed_actions


def get_token_claims(request_params):
    """Get token for user"""
    claims = {
        'iss': 'sergbelom',
        'nbf': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    if 'service' in request_params:
        claims['aud'] = request_params['service'][0]  
    if 'scope' in request_params:
        LOG.debug('client requesting access: %s', request_params['scope'])
        claims['access'] = get_allowed_actions(request_params)
    return claims


@app.route('/api/auth')
def auth():
    request_params = dict(request.args)
    LOG.debug("auth called: %s", request_params)
    LOG.debug("headers: %s", request.headers)
    if not 'Authorization' in request.headers:
        return response(401, {'error': 'basic auth required'})
    auth_header = re.match(r'Basic (\S+)', request.headers['Authorization'])
    if not auth_header:
        return response(401, {'error': 'malformed Authorization header'})
    user, password = base64.b64decode(auth_header.group(1)).split(':')
    if user in AUTH_STORE and AUTH_STORE[user] == password:
        keyid = key_id_algorithm(SIGNKEY)        
        signed_token = jwt.encode(
            get_token_claims(request_params), SIGNKEY, algorithm='RS256',
            headers={'kid': keyid})
        LOG.debug("key id: '%s'" % keyid)
        LOG.debug("responding with token: %s" % signed_token)
        return response(200, {"token": signed_token})
    else:
        return response(401, {'error': 'incorrect username/password'})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", default=AUTH, help='Dictionary of form {"user": "password", ... }.')
    parser.add_argument("--port", type=int, default=5001, help="HTTPS port.")
    parser.add_argument("--cert", default=CERT, help="TLS cert (PEM file).")
    parser.add_argument("--key",  default=KEY, help="TLS key (PEM file).")
    args = parser.parse_args()

    with open(args.auth) as authfile:
        AUTH_STORE = json.load(authfile)
        LOG.info(AUTH_STORE)

    if not os.path.isfile(args.cert):
        LOG.error("cert file does not exist")
        raise FileExistsError
   
    if not os.path.isfile(args.key):
        LOG.error("key file does not exist")
        raise FileExistsError

    with open(args.key) as keyfile:
        SIGNKEY = keyfile.read()
    
    ssl_cert = (args.cert, args.key)
    app.run(
        host='0.0.0.0', port=args.port,
        ssl_context=ssl_cert, threaded=True)
