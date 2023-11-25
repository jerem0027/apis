#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from core.identity import check_identity, generate_APIKEY
from core.utils import encode_pass
from db.db_home_users import User_DB
from errors.errors import ObjectNotFound, TokenError
from flask_restx import Resource
from models.model_home_user import (model_home_update, model_home_user,
                                    model_home_user_password)
from server.instance import server

from flask import request

app, api, db = server.app, server.api, server.db

home_db_ns = api.namespace(
    name='home_user',
    description='Manage user home website'
)

@home_db_ns.response(500, 'Internal Server Error')
@home_db_ns.response(404, 'User not found')
@home_db_ns.response(403, 'Error with Database')
@home_db_ns.response(401, 'Invalide Access Token')
@home_db_ns.route("/user/<string:pseudo>")
class Home_users_pseudo(Resource):
    @home_db_ns.response(200, 'User found')
    @home_db_ns.response(201, 'User not found')
    def get(self, pseudo):
        """
        check_username
        """
        if User_DB(pseudo=pseudo).check_pseudo():
            return {"status": "User found"}, 200
        raise ObjectNotFound("User not found")

@home_db_ns.response(500, 'Internal Server Error')
@home_db_ns.response(403, 'Error with Database')
@home_db_ns.response(401, 'Invalide Access Token')
@home_db_ns.route("/user/")
class Home_users(Resource):
    @home_db_ns.response(200, 'User created successfully')
    @home_db_ns.expect(model_home_user)
    def post(self):
        """
        Create user
        """
        if not check_identity().get("access_plus", False) == True:
            raise TokenError("Access denied")
        user:dict = request.json
        User_DB(
            pseudo=user.get("pseudo"),
            first_name=user.get("first_name").capitalize(),
            name=user.get("name").capitalize(),
            email=user.get("email"),
            password=encode_pass(user.get("password")),
            birthdate=datetime.strptime(user.get("birthdate"), '%d-%m-%Y'),
            inscription_date=datetime.strptime(datetime.now().strftime('%d-%m-%Y'),'%d-%m-%Y')
        ).create()

        return {"status": "User created successfully", "APIKEY": generate_APIKEY({"pseudo": user.get("pseudo")})}, 200

    @home_db_ns.response(200, 'User data send')
    def get(self):
        """
        Get user data
        """
        pseudo = check_identity().get("pseudo", "")
        user_data = User_DB(pseudo=pseudo).get().to_dict()
        if not user_data:
            raise ObjectNotFound(f"User '{pseudo}' not found")

        return {"status": "Guest found", "content": user_data}, 200

    @home_db_ns.response(200, 'User removed')
    def delete(self):
        """
        Delete user
        """
        pseudo = check_identity().get("pseudo", "")
        User_DB(pseudo=pseudo).delete()

        return {"status": f"User '{pseudo}' deleted successfully"}, 200

    @home_db_ns.response(200, 'User data updated')
    @home_db_ns.expect(model_home_update)
    def put(self):
        """
        Update user
        """
        pseudo = check_identity().get("pseudo", "")
        user:dict = request.json
        User_DB(
            pseudo=pseudo,
            first_name=user.get("first_name").capitalize() if type(user.get("first_name", None)) == str else None,
            name=user.get("name").capitalize() if type(user.get("name", None)) == str else None,
            email=user.get("email", None),
            birthdate=datetime.strptime(user.get("birthdate"), '%d-%m-%Y') if type(user.get("birthdate", None)) == str else None
        ).update()

        return {"status": "User updated successfully"}, 200

@home_db_ns.response(500, 'Internal Server Error')
@home_db_ns.response(403, 'Error with Database')
@home_db_ns.response(401, 'Invalide Access Token')
@home_db_ns.route("/user/password/")
class Home_users_password(Resource):
    @home_db_ns.response(200, 'User created successfully')
    @home_db_ns.expect(model_home_user_password)
    def put(self):
        """
        Update user password
        """
        pseudo = check_identity().get("pseudo", "")
        User_DB(
            pseudo=pseudo,
            password=encode_pass(request.json.get("password")),
        ).update()

        return {"status": f"User '{pseudo}' password updated successfully"}, 200