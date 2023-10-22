#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.util import strtobool

from core.colors import green

API_VERSION = "1.0.3"
BASE_URL = "/api/v1"


DEBUG = strtobool(os.environ.get("FLASK_DEBUG", "False"))
ENV = os.environ.get("ENV", "production")

if DEBUG:
    ENV = "develop"
    print(green("!!! DEBUG MODE ACTIVÉ !!!"))

# Path root
PATH_ROOT = os.environ.get("PATH_ROOT", "")
ICON = os.path.join(PATH_ROOT, "static/icon_blue.png")

# Folder creation files
FILE_FOLDER = os.path.join(PATH_ROOT, "files")

# Unused
LOG_FILE = PATH_ROOT + "/log.log"


# Configuration envoi Mail
class configMail:
    MAIL_PORT = 587
    SMTP_SERVER = "smtp.gmail.com"
    SENDER_EMAIL = "envoimailpython@gmail.com"
    PASSWORD = os.getenv("MAILPASS")

## Configuration connection DB
class confdb:
    DB_USER = "root"
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = "3306"

    db_santa_name = "home_secret_santa"
    db_home_name = "home_db"
    db_test_name = "home_tests"

class confAuth:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-Secret-Key")
    JWT_ACCESS_TOKEN_EXPIRES = 10800
