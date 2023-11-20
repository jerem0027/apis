#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity, generate_APIKEY, generate_MASTERKEY
from core.utils import decode_pass
from db.db_home_users import User_DB
from errors.errors import ObjectNotFound, TokenError
from flask_restx import Resource, fields
from models.model_home_user import model_home_user_connection
from server.instance import server

from flask import request

api = server.api

identity_model = api.model('identity',{
    'pseudo': fields.String(
        required=True,
        title='Pseudo',
        example='dark_lord',
        description='User pseudo'
    ),
})

identity = api.namespace(
    name='identity',
    description='Identity namespace'
)

@identity.response(500, 'Internal Server Error')
@identity.response(400, 'Missing parameter')
@identity.route("/")
class Identity(Resource):
    @identity.response(200, 'APIKEY accepted')
    def get(self):
        """
        check identity and access validity to API
        """
        return check_identity(), 200

    @identity.response(200, 'New APIKEY generated')
    @identity.expect(identity_model)
    def post(self):
        """
        Generate APIKEY
        """
        if not "masterkey" in check_identity():
            raise TokenError("Access denied")
        return { "APIKEY": generate_APIKEY(request.json)}, 200

    @identity.response(200, 'New MASTERKEY generated')
    def patch(self):
        """
        Generate MASTER APIKEY (only for admin)
        """
        return { "APIKEY": generate_MASTERKEY(check_identity())}, 200
    
@identity.response(500, 'Internal Server Error')
@identity.response(404, 'User not found')
@identity.response(403, 'Error with Database')
@identity.response(401, 'Invalide Access Token')
@identity.route("/connection/")
class Home_users_connection(Resource):
    @identity.response(200, 'Password march successfully')
    @identity.expect(model_home_user_connection)
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
        if not decode_pass(user.get("password"), user_bd.get().password):
            raise ObjectNotFound("Password doesn't match")
        return {"message": "Success, Password matched", "APIKEY": generate_APIKEY({"pseudo": user.get("pseudo")}), "pseudo": user.get("pseudo")}, 200