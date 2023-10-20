#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
class FileError(APIError):
    pass