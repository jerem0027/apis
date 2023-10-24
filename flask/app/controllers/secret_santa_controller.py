#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity
from db.db_secret_santa import Guest_DB
from errors.handlers import *
from flask_restx import Resource
from models.model_demande import *
from models.model_guest import guest_model
from server.envconfig import *
from server.instance import server

from flask import request

app, api, db = server.app, server.api, server.db

secret_santa = api.namespace(
    name='secret_santa',
    description='Secret santa managing (guest and user)'
)

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.route("/guest")
class Guest(Resource):
    @secret_santa.response(200, 'Function ok')
    def get(self):
        """
        Get all guest
        """
        check_identity()
        guests = Guest_DB.query.all()
        return {
            "status": "this is a test",
            "content": [str(guest) for guest in guests]
        }, 200

    @secret_santa.response(200, 'Function ok')
    @secret_santa.expect(guest_model)
    def post(self):
        """
        Create new guest
        """
        check_identity()
        guest = Guest_DB.add_guest(request.json)
        return {
            "status": f"New guest added successfully",
            "content": guest
        }, 200

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.route("/guest/<string:lien>")
class Guest_lien(Resource):

    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(404, 'Link not found')
    def get(self, lien:str):
        """
        Get guest from Link
        """
        guest = Guest_DB.get_guest(lien)
        return {
            "status": "Guest found",
            "name": guest.get("name"),
            "email": guest.get("email"),
            "target": guest.get("target"),
            "target_email": guest.get("target_email")
        }, 200
