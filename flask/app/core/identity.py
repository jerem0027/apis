#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from core.colors import green
from errors.errors import ObjectNotFound, TokenError
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from server.envconfig import DEBUG, confAuth

from flask import request


def check_identity() -> dict:
    apikey = request.headers.get("APIKEY", {})

    if DEBUG:
        print(green("!!! Authentification in DEBUG mode !!!"))
        return {"masterkey": True, "access_plus": True, "pseudo": "test"}

    if not apikey:
        raise ObjectNotFound("Please set your APIKEY")
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
            algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise TokenError("Signature expired. Please log in again.")
    except InvalidTokenError:
        raise TokenError("Invalid token. Please log in again.")

def generate_APIKEY(user_data:dict) -> str:
    """
    Generate apikey auth token
    :param user_data:
    """
    payload = {
        "exp": datetime.utcnow() + timedelta(seconds=confAuth.JWT_ACCESS_TOKEN_EXPIRES),
        "iat": datetime.utcnow()
    }
    if not DEBUG:
        for key in ["masterkey", "exp", "iat", "access_plus"]:
            if user_data.get(key, None):
                user_data.pop(key)

    payload.update(user_data)
    return encode(payload, confAuth.JWT_SECRET_KEY, algorithm="HS256")

def generate_MASTERKEY(payload:dict, master:bool=False) -> str:
    """
    Generate apikey auth token
    :param user_data:
    """
    if not payload.get("masterkey", None):
        raise TokenError("Access Denied")
    delta = timedelta(seconds=confAuth.JWT_MASTER_ACCESS_TOKEN_EXPIRES) if not master else timedelta(days=90)
    refresh = {
        "exp": datetime.utcnow() + delta,
        "iat": datetime.utcnow(),
        "access_plus": True,
    }
    if master:
        refresh.update({"masterkey": True})
    return encode(refresh, confAuth.JWT_SECRET_KEY, algorithm="HS256")