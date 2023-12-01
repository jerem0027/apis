#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 401 -> Token ERROR
# 402 -> File ERROR
# 403 -> DB ERROR
# 404 -> Not Found ERROR
# 499 -> API ERROR
# 500 -> Exception catched

class APIError(Exception):
    pass
class ObjectNotFound(APIError):
    pass
class TokenError(APIError):
    pass
class YamlError(APIError):
    pass
class DBError(APIError):
    pass
class Unauthorized(APIError):
    pass
class FileError(APIError):
    pass
class RequestError(APIError):
    pass