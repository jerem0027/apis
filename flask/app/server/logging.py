#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import socket
import time

from core.colors import cyan, green, orange, purple, red
from flask import g, request

from .instance import server


@server.app.before_request
def start_time():
    g.start = time.time()

@server.app.after_request
def log_request(response):
    now = time.time()
    duration = round(now - g.start, 2)
    # sender = socket.gethostname()
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # host = request.host.split(':', 1)[0]
    args = dict(request.args)
    code = orange(response.status_code)
    if 200 <= response.status_code <= 299:
        code = green(response.status_code)
    if 400 <= response.status_code <= 499:
        code = red(response.status_code)
    log_params = [
        # ('sender', sender),
        ('client_ip', cyan(client_ip)),
        # ('host', host),
        ('method', orange(request.method)),
        ('path', request.path),
        ('params', args),
        ('payload', request.data),
        ('status', code),
        ('response', purple(response.json)),
        ('duration', duration)
    ]

    parts = []
    for name, value in log_params:
        part = f"{name}={value}"
        parts.append(part)
    line = " ".join(parts)

    if 400 <= response.status_code <= 499:
        server.app.logger.warning(line)
    elif 200 <= response.status_code <= 299 and "swagger.json" not in request.path:
        server.app.logger.info(line)
    return response
