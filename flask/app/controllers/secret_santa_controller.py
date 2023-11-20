#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from core.identity import check_identity
from core.secret_santa import create_associations
from db.db_secret_santa import Guest_DB, Secret_santa_DB
from flask_restx import Resource
from models.model_secret_santa import form_secret_santa
from server.instance import server

from flask import request

app, api, db = server.app, server.api, server.db

secret_santa = api.namespace(
    name='secret_santa',
    description='Secret santa managing (guest and user)'
)

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.route("/guest/<string:link>")
class Guest_link(Resource):

    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(404, 'Link not found')
    def get(self, link:str):
        """
        Get guest from Link
        """
        guest = Guest_DB(link=link).get()

        return {"status": "Guest found", "content": guest}, 200

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.route("/create")
class Secret_Santa(Resource):
    @secret_santa.response(200, 'Function ok')
    @secret_santa.expect(form_secret_santa)
    def post(self):
        """
        Create new secret santa
        """
        creator = check_identity().get("pseudo", "")
        guests = create_associations(request.json.get("guests"))
        secret_santa_id = Secret_santa_DB(
            name=request.json.get("title"),
            creator=creator,
            date_end=datetime.strptime(request.json.get("date_end"), '%d-%m-%Y')
        ).create()

        for guest in guests:
            Guest_DB(
                secret_santa_id=secret_santa_id,
                name=guest.get("name"),
                email=guest.get("email"),
                target=guest.get("target"),
                target_email=guest.get("target_email")
            ).create()

        return {"status": "Secret Santa created successfully"}, 200

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.response(405, 'Action Unauthorized')
@secret_santa.route("/<int:id>")
class Secret_Santa_Data(Resource):
    @secret_santa.response(200, 'Function ok')
    def get(self, id:int):
        """
        Get secret santa informations
        """
        check_identity()
        secret_santa = Secret_santa_DB(id=id).get()
        guests = Secret_santa_DB(id=id).list_guests()
        secret_santa["guests"] = list()

        for guest in guests:
            tmp_dict = guest.to_dict()
            tmp_dict.pop("link"),
            tmp_dict.pop("target"),
            tmp_dict.pop("target_email")
            secret_santa["guests"].append(tmp_dict)
        return {"status": "Secret Santa found", "content": secret_santa}, 200

    @secret_santa.response(200, 'Function ok')
    def delete(self, id:int):
        """
        Delete secret santa and every guest associated
        """
        pseudo = check_identity().get("pseudo", "")
        Secret_santa_DB(id=id, creator=pseudo).delete()
        return {"status": "Secret Santa deleted successfully"}, 200