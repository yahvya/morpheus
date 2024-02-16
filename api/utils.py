##
# @brief point d'entrée de les utils du projet Morpheus
# @author Vitalli https://github.com/siegward-from
import hmac
import hashlib
import base64
import time

from fastapi import Request, HTTPException
import secrets


def generate_signature(data, secret_key):
    message = data.encode('utf-8')
    secret = secret_key.encode('utf-8')

    signature = hmac.new(secret, message, hashlib.sha256).digest()
    signature_base64 = base64.urlsafe_b64encode(signature).decode('utf-8')

    return signature_base64


def check_signature(request: Request):
    try:
        signature = request.headers['signature']
    except KeyError:
        raise HTTPException(status_code=400, detail='signature is missing')

    try:
        data = request.headers['data']
    except KeyError:
        raise HTTPException(status_code=400, detail='data is missing')

    with open('key', 'r') as f:
        key = f.read()

    if not signature or not data or not key:
        raise HTTPException(status_code=400, detail='Bad request')

    signature_generated = generate_signature(data, key)

    print(signature_generated)

    if not hmac.compare_digest(signature, signature_generated):
        raise HTTPException(status_code=401, detail="Invalid signature")


def generate_secret_key(length=32):
    with open('key', 'w') as f:
        key = secrets.token_hex(length)
        f.write(key)


def check_signature_with_timestamp(request: Request, tolerance = 300):
    try:
        signature = request.headers['signature']
    except KeyError:
        raise HTTPException(status_code=400, detail='signature is missing')

    try:
        data = request.headers['data']
    except KeyError:
        raise HTTPException(status_code=400, detail='data is missing')

    try:
        timestamp = request.headers['timestamp']
    except KeyError:
        raise HTTPException(status_code=400, detail='timestamp is missing')

    with open('key', 'r') as f:
        key = f.read()

    signed_data = f'{timestamp}.{data}'
    hmac_signature = generate_signature(signed_data, key)

    if hmac.compare_digest(hmac_signature, signature):
        current_diff = time.time() - int(timestamp)
        return not (current_diff < 0 or current_diff > tolerance)

    return False


