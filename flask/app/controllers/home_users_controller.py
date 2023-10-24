#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity, generate_APIKEY
from core.utils import decode_pass, encode_pass
from db.db_home_users import User_DB
from errors.errors import ObjectNotFound, TokenError
from flask_restx import Resource
from models.model_home_user import model_home_user, model_home_user_connection
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
            return {"message": "User found"}, 200
        raise ObjectNotFound("User not found")

@home_db_ns.response(500, 'Internal Server Error')
@home_db_ns.response(404, 'User not found')
@home_db_ns.response(403, 'Error with Database')
@home_db_ns.response(401, 'Invalide Access Token')
@home_db_ns.route("/user/connection")
class Home_users_connection(Resource):
    @home_db_ns.response(200, 'Password march successfully')
    @home_db_ns.expect(model_home_user_connection)
    def put(self):
        """
        check connection validity
        """
        if not "masterkey" in check_identity():
            raise TokenError("Access denied")
        user:dict = request.json
        user_bd = User_DB(
            pseudo=user.get("pseudo")
        )
        if not user_bd.check_pseudo():
            raise ObjectNotFound("User not found")
        if not decode_pass(user.get("password"), user_bd.get_user().password):
            raise ObjectNotFound("Password doesn't match ok")
        return {"message": "Success, Password matched", "APIKEY": generate_APIKEY({"pseudo": user.get("pseudo")})}, 200

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
        if not "masterkey" in check_identity():
            raise TokenError("Access denied")
        user:dict = request.json
        User_DB(
            pseudo=user.get("pseudo"),
            first_name=user.get("first_name").capitalize(),
            name=user.get("name").capitalize(),
            email=user.get("email"),
            password=encode_pass(user.get("password"))
        ).add_user()
        return {"message": "Success, User created", "APIKEY": generate_APIKEY({"pseudo": user.get("pseudo")})}, 200
