##
# @brief point d'entrée de les utils du projet Morpheus
# @author Vitalli https://github.com/siegward-from

import hmac
import hashlib
import base64
import time
from fastapi import Request, HTTPException
import secrets
import os


def generate_signature(key: bytes, files) -> str:
    hmac_sha256 = hmac.new(key.encode(), digestmod=hashlib.sha256)
    for file_path in files:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hmac_sha256.update(chunk)
    return hmac_sha256.hexdigest()


async def save_upload_file(directory: str, file):
    file_location = f"{directory}/{file.filename}"
    with open(file_location, "wb") as buffer:
        data = await file.read()
        buffer.write(data)
    return file_location


async def save_files(files):
    video_dir = '.\\videos'
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)

    video_paths = []
    for video in files:
        path = await save_upload_file(video_dir, video)
        video_paths.append(path)

    return video_paths


def check_signature(data, signature):
    secret_key = 'c27f9aad7c97689dffe026a2482bb3878dffbe78ae0e79e90638c72fcc545227'
    signature_generated = generate_signature(secret_key, data)
    if signature != signature_generated:
        raise HTTPException(status_code=400, detail='signature is missing')
    else:
        print('Signature verification passed')


def generate_base_signature(data, secret_key):
    message = data.encode('utf-8')
    secret = secret_key.encode('utf-8')

    signature = hmac.new(secret, message, hashlib.sha256).digest()
    signature_base64 = base64.urlsafe_b64encode(signature).decode('utf-8')

    return signature_base64


def check_base_signature(request: Request):
    try:
        signature = request.headers['signature']
    except KeyError:
        raise HTTPException(status_code=400, detail='signature is missing')

    try:
        data = request.headers['data']
    except KeyError:
        raise HTTPException(status_code=400, detail='data is missing')

    key = get_secret_key()

    if not signature or not data or not key:
        raise HTTPException(status_code=400, detail='Bad request')

    signature_generated = generate_signature(data, key)

    print(signature_generated)

    if not hmac.compare_digest(signature, signature_generated):
        raise HTTPException(status_code=401, detail="Invalid signature")


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


def generate_secret_key(length=32):
    with open('key', 'w') as f:
        key = secrets.token_hex(length)
        f.write(key)


def get_secret_key():
    with open('key', 'r') as f:
        key = f.read()
    return key
