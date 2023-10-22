#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, Flask, Response, redirect, request, send_file,
                   url_for)
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from .envconfig import API_VERSION, BASE_URL, DEBUG, ENV, ICON, confdb


class Server:

    authorizations = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "APIKEY",
            "description": "APIKEY: <access_token>"
        }
    }

    def __init__(self) -> None:
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.app.config["CORS_HEADERS"] = "Content-Type"
        self.app.config['ERROR_404_HELP'] = False
        self.app.config["JSON_SORT_KEYS"] = False
        self.app.config["PREFERRED_URL_SCHEME"] = "https"
        #self.app.config["UPLOAD_FOLDER"] = PATH_TO_UPLOAD_FOLDER

        # Configuration de la DB
        self.app.config['SQLALCHEMY_BINDS'] = {
            ## DB DE TEST
            confdb.db_test_name: f"mysql+pymysql://{confdb.DB_USER}:{confdb.DB_PASSWORD}@{confdb.DB_HOST}:{confdb.DB_PORT}/{confdb.db_test_name}",
            ## DB SECRET SANTA
            confdb.db_santa_name: f"mysql+pymysql://{confdb.DB_USER}:{confdb.DB_PASSWORD}@{confdb.DB_HOST}:{confdb.DB_PORT}/{confdb.db_santa_name}",
            ## DB HOME
            confdb.db_home_name: f"mysql+pymysql://{confdb.DB_USER}:{confdb.DB_PASSWORD}@{confdb.DB_HOST}:{confdb.DB_PORT}/{confdb.db_home_name}"
        }
        self.app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = SQLAlchemy(self.app)

        if ENV != "develop":
            @property
            def specs_url(self) -> str:
                return url_for(self.endpoint("specs"), _external=True, _scheme="https")
            Api.specs_url = specs_url

        blueprint = Blueprint("api", __name__, url_prefix=BASE_URL)
        self.api = Api(
            app=blueprint,
            title="J.API",
            version=API_VERSION,
            description="Jeremie API - Api dédié à la partie Secret Santa du site\n\n<a href=\"/home/\">back Home</a>",
            authorizations=self.authorizations,
            security="apikey"
        )
        self.app.register_blueprint(blueprint)

    def run(self) -> None:
        self.app.run()

server = Server()

@server.app.route("/status")
def status() -> set:
    return {"OK", 200}

@server.app.route("/")
def index() -> Response:
    return redirect(BASE_URL)

@server.app.before_request
def before_request() -> Response | None:
    if request.url.startswith("http://") and not (DEBUG or ENV=="develop"):
        url = request.url.replace("http://", "https://", 1)
        return redirect(url)

@server.app.route("/swaggerui/favicon-16x16.png")
@server.app.route("/swaggerui/favicon-32x32.png")
def favicon3() -> Response:
    return send_file(open(os.path.join(ICON), 'rb'), mimetype="image/png")
