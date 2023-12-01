#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.util import strtobool

from core.colors import green

API_VERSION = "1.2.0"
BASE_URL = "/api/v1"
DESCRIPTION = f"""
<h2>API dédié à la partie Secret Santa du site</h2>
<h4>Pour retourner sur le site cliquer ici <a href="/home/">HOME</a></h4>

<h4>Vous pouvez trouver la derniere release note ici: <a href="{BASE_URL}/changelog">CHANGELOG</a></h4>
"""

DEBUG = strtobool(os.environ.get("FLASK_DEBUG", "False"))
ENV = os.environ.get("ENV", "production")

if DEBUG:
    ENV = "develop"
    print(green("!!! DEBUG MODE ACTIVÉ !!!"))

# Path root
PATH_ROOT = os.environ.get("PATH_ROOT", "")
ICON = os.path.join(os.getcwd(), "static/icon_blue.png")

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

    db_santa_name = "home_tests" # "home_secret_santa"
    db_home_name = "home_tests" # "home_db"
    db_test_name = "home_tests" # "home_tests"

class confAuth:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-Secret-Key")
    JWT_ACCESS_TOKEN_EXPIRES = 10800
    JWT_MASTER_ACCESS_TOKEN_EXPIRES = 100
