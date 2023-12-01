#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from core.identity import check_identity
from core.secret_santa import create_associations
from db.db_home_users import User_DB
from db.db_secret_santa import Guest_DB, Secret_santa_DB
from errors.errors import DBError, RequestError
from flask_restx import Resource
from models.model_secret_santa import (form_secret_santa,
                                       form_update_guest_gift,
                                       form_update_secret_santa)
from server.instance import server
from werkzeug.exceptions import BadRequest

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
        Get guest information from Link
        """
        guest = Guest_DB(link=link).get()
        target = Guest_DB(link=guest.target_link).get().to_dict()
        secret_santa = Secret_santa_DB(id=guest.secret_santa_id).get()
        creator = User_DB(pseudo=secret_santa.creator).get()

        guest = guest.to_dict()
        guest.update({
            "secret_santa": secret_santa.name,
            "date_end": str(secret_santa.date_end),
            "nb_guest": len(secret_santa.list_guests()),
            "creator_name": creator.name,
            "creator_email": creator.email,
            "target_name": target["name"],
            "target_email": target["email"],
            "target_gift_list": target["gift_list"]
        })
        guest.pop("link")
        guest.pop("target_link")
        return {"status": "Guest found", "content": guest}, 200

    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(404, 'Link not found')
    @secret_santa.expect(form_update_guest_gift)
    def put(self, link:str):
        """
        Update guest information from Link
        """
        gift_list = request.json.get("gift_list", [])
        Guest_DB(
            link=link,
            user=request.json.get("user", None),
            gift1=gift_list[0].capitalize() if len(gift_list) > 0 else None,
            gift2=gift_list[1].capitalize() if len(gift_list) > 1 else None,
            gift3=gift_list[2].capitalize() if len(gift_list) > 2 else None,
            gift4=gift_list[3].capitalize() if len(gift_list) > 3 else None,
            gift5=gift_list[4].capitalize() if len(gift_list) > 4 else None
        ).update()
        return {"status": "Guest updated successfully"}, 200

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.route("/guest/list/")
class Guest_list(Resource):
    @secret_santa.response(200, 'Function ok')
    @secret_santa.response(404, 'Link not found')
    def get(self):
        """
        Get list of secret santa where your are guest and guest link associated
        """
        user = check_identity().get("pseudo", "")
        guests = Guest_DB(user=user).list_guest()
        rtn = list()
        for guest in guests:
            sesa = Secret_santa_DB(id=guest.secret_santa_id).get()
            if sesa.creator == user:
                continue
            sesa = sesa.to_dict()
            sesa["link"] = guest.link
            rtn.append(sesa)
        return {"status": "Guests found", "content": rtn}, 200

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.route("/")
class Secret_Santa(Resource):
    @secret_santa.response(200, 'Function ok')
    @secret_santa.expect(form_secret_santa)
    def post(self):
        """
        Create new secret santa
        """
        creator = check_identity().get("pseudo", "")
        email = User_DB(pseudo=creator).get().email
        secret_santa_id = Secret_santa_DB(
            name=request.json.get("title").capitalize(),
            creator=creator,
            date_end=datetime.strptime(request.json.get("date_end"), '%d-%m-%Y')
        ).create()

        to_break = False
        list_guest:list[Guest_DB] = []
        retry = 0
        while True:
            if retry >= 3:
                raise DBError("Error during creation of new secret santa")
            retry+=1
            to_break = False
            guests = create_associations(request.json.get("guests"))
            for i, guest in enumerate(guests):
                list_guest.append(Guest_DB(
                    link=guest.get("link"),
                    secret_santa_id=secret_santa_id,
                    name=guest.get("name"),
                    email=guest.get("email").lower(),
                    target_link=guest.get("target_link"),
                    user=creator if email == guest.get("email", "").lower() else None
                ))
                try:
                    if list_guest[i].get():
                        to_break = True
                        list_guest = []
                        break
                except:
                    pass
            if to_break or len(list_guest) == len(guests):
                break

        for guest in list_guest:
            guest.create()
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
        secret_santa = Secret_santa_DB(id=id).get().to_dict()
        guests = Secret_santa_DB(id=id).list_guests()
        secret_santa["guests"] = list()

        for guest in guests:
            tmp_dict = guest.to_dict()
            for e in ["link", "target_link", "gift_list"]:
                tmp_dict.pop(e)
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

    @secret_santa.response(200, 'Function ok')
    @secret_santa.expect(form_update_secret_santa)
    def put(self, id:int):
        """
        Update secret santa
        """
        creator = check_identity().get("pseudo", "")
        date, name = None, None
        try:
            date = request.json.get("date_end", None)
            name = request.json.get("title", None)
        except BadRequest:
            raise RequestError("Json date not found")
        Secret_santa_DB(
            id=id,
            name=name,
            creator=creator,
            date_end=datetime.strptime(date, '%d-%m-%Y') if date else None
        ).update()
        return {"status": "Secret Santa updated successfully"}, 200

@secret_santa.response(500, 'Internal Server Error')
@secret_santa.response(403, 'Error with Database')
@secret_santa.response(405, 'Action Unauthorized')
@secret_santa.route("/list/")
class Secret_Santa_Data(Resource):
    @secret_santa.response(200, 'Function ok')
    def get(self):
        """
        Get secret santa list from user and guest link associated
        """
        user = check_identity().get("pseudo", "")
        secret_santa = Secret_santa_DB(creator=user).list_secret_santa()
        rtn = list()
        for sesa in secret_santa:
            guest = Guest_DB(secret_santa_id=sesa.id, user=user).get_guest_from_sesa()
            if not guest:
                continue
            tmp = sesa.to_dict()
            tmp["link"] = guest.link
            rtn.append(tmp)
        return {"status": "Secret Santa found", "content": rtn}, 200