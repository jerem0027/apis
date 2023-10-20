#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from core.colors import green
from errors.errors import ObjectNotFound, TokenError
from flask import request
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from server.envconfig import DEBUG, confAuth


def check_identity():
    if DEBUG:
        print(green("!!! Authentification in DEBUG mode !!!"))
        return True

    apikey = request.headers.get('APIKEY', None)
    if not apikey:
        raise ObjectNotFound('Please set your APIKEY')
    return check_APIKEY(apikey)

def check_APIKEY(apikey) -> dict:
    """
    Decode apikey auth token
    :param apikey:
    """
    try:
        payload = decode(
            jwt=apikey,
            key=confAuth.JWT_SECRET_KEY,
            algorithms=['HS256'])
        return payload
    except ExpiredSignatureError:
        raise TokenError("Signature expired. Please log in again.")
    except InvalidTokenError:
        raise TokenError("Invalid token. Please log in again.")

def generate_APIKEY(user_data:dict):
    """
    Generate apikey auth token
    :param user_data:
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=confAuth.JWT_ACCESS_TOKEN_EXPIRES),
        'iat': datetime.utcnow()
    }
    if not DEBUG:
        for key in user_data.keys():
            if key in ["masterkey", "exp", "iat"]:
                raise TokenError("Invalid token data")
    payload.update(user_data)
    return encode(payload, confAuth.JWT_SECRET_KEY, algorithm='HS256'), 200

def generate_MASTERKEY(payload):
    """
    Generate apikey auth token
    :param user_data:
    """
    if not payload.get("masterkey", None):
        raise TokenError("Access Denied")
    refresh = {
        'exp': datetime.utcnow() + timedelta(days=90),
        'iat': datetime.utcnow()
    }
    payload.update(refresh)
    return encode(payload, confAuth.JWT_SECRET_KEY, algorithm='HS256'), 200