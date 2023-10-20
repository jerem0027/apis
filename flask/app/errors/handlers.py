#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket
import time
import traceback

from errors.errors import (APIError, DBError, FileError, ObjectNotFound,
                           TokenError)
from flask import g, request
from server.instance import server
from werkzeug.exceptions import InternalServerError

app, api = server.app, server.api

# 401 -> Token ERROR
# 402 -> File ERROR
# 403 -> DB ERROR
# 404 -> Not Found ERROR
# 499 -> API ERROR
# 500 -> Exception catched

@api.errorhandler(TokenError)
def handle_token_error(e):
    logging.error(str(e))
    code = 401
    type = e.__class__.__name__
    response = {
        "error": {
            "message": str(e),
            "type": type,
            "code": code
        }
    }
    return response, code

@api.errorhandler(FileError)
def handle_error_database(e):
    logging.error(str(e))
    code = 402
    type = e.__class__.__name__
    response = {
        "error": {
            "message": str(e),
            "type": type,
            "code": code
        }
    }
    return response, code

@api.errorhandler(DBError)
def handle_database_error(e):
    logging.error(str(e))
    code = 403
    type = e.__class__.__name__
    response = {
        "error": {
            "message": str(e),
            "type": type,
            "code": code
        }
    }
    return response, code

@api.errorhandler(ObjectNotFound)
def handle_object_not_found(e):
    logging.error(str(e))
    code = 404
    type = e.__class__.__name__
    response = {
        "error": {
            "message": str(e),
            "type": type,
            "code": code
        }
    }
    return response, code

@api.errorhandler(APIError)
def handle_error(e):
    code = 499
    type = e.__class__.__name__
    response = {
        "error": {
            "message": str(e),
            "type": type,
            "code": code,
            "info": "undefined error"
        }
    }
    return response, code

@api.errorhandler(Exception)
@api.errorhandler(InternalServerError)
def handle_default_exception(e):
    code = 500
    type = e.__class__.__name__
    response = {
        "error": {
            "message": str(e),
            "type": type,
            "code": code
        }
    }

    now = time.time()
    duration = round(now - g.start, 2)
    sender = socket.gethostname()
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)
    tb = traceback.format_exc()

    log_params = [
        ('sender', sender),
        ('client_ip', client_ip),
        ('host', host),
        ('method', request.method),
        ('path', request.path),
        ('params', args),
        ('payload', request.data),
        ('status', code),
        ('response', response),
        ('duration', duration),
        ('traceback', tb)
    ]

    parts = []
    for name, value in log_params:
        part = f"{name}={value}"
        parts.append(part)
    line = " ".join(parts)

    server.api.logger.error(line)

    return response, code