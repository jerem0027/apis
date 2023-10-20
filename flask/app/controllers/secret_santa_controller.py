#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity
from db.db_secret_santa import Guest_DB, User
from errors.handlers import *
from flask import request
from flask_restx import Resource
from models.model_demande import *
from models.model_guest import guest_model
from models.model_secret_santa import form_users
from server.envconfig import *
from server.instance import server

app, api, db = server.app, server.api, server.db

secret_santa = api.namespace(
    name='secret_santa',
    description='Secret santa managing (guest and user)'
)

@secret_santa.response(500, 'Internal error')
@secret_santa.route("/guest")
class Guest(Resource):
    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(405, 'Error with Database')
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
    @secret_santa.response(405, 'Error with Database')
    @secret_santa.expect(guest_model)
    def put(self):
        """
        Create new guest
        """
        check_identity()
        guest = Guest_DB.add_guest(request.json)
        return {
            "status": f"New guest added successfully",
            "content": guest
        }, 200

@secret_santa.response(500, 'Internal error')
@secret_santa.route("/guest/<string:lien>")
class Guest_lien(Resource):

    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(404, 'Link not found')
    @secret_santa.response(405, 'Error with Database')
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

@secret_santa.response(500, 'Internal error')
@secret_santa.route("/get_all")
class Santa_all(Resource):
    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(400, 'Missing parameter')
    def get(self):
        """
        test namespace
        """
        tests = User.query.all()
        data = [
            { test.id: test.name } for test in tests]
        return {
            "status": "this is a test",
            "content": data
            }, 200

    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(405, 'Key already exist')
    @secret_santa.expect(form_users, validate=True)
    def put(self):
        """
        Creation d'un utilisateur
        """
        name = api.payload
        data = User(name["name"])
        data.add_user()
        return {
            "status": "User created",
            "user": data.name,
            "id": data.id
            }, 200
