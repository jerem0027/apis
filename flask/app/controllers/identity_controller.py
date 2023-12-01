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
        example='test',
        description='User pseudo'
    ),
})

identity = api.namespace(
    name='identity',
    description='Identity namespace'
)

@identity.response(500, 'Internal Server Error')
@identity.response(404, 'User not found')
@identity.response(403, 'Error with Database')
@identity.response(401, 'Invalide Access Token')
@identity.route("/connection/")
class Identity(Resource):
    @identity.response(200, 'Password march successfully')
    @identity.expect(model_home_user_connection)
    def put(self):
        """
        check connection validity
        """
        if not check_identity().get("access_plus", False) == True:
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

@identity.response(500, 'Internal Server Error')
@identity.response(400, 'Missing parameter')
@identity.route("/apikey/")
class Apikey(Resource):
    @identity.response(200, 'APIKEY accepted')
    def get(self):
        """
        Check identity and access validity to API
        """
        return check_identity(), 200

    @identity.response(200, 'New APIKEY generated')
    @identity.expect(identity_model)
    def post(self):
        """
        Génerate new apikey (admin only)
        """
        if not check_identity().get("access_plus", False) == True:
            raise TokenError("Access denied")
        return { "APIKEY": generate_APIKEY(request.json)}, 200

@identity.response(500, 'Internal Server Error')
@identity.response(400, 'Missing parameter')
@identity.route("/apikey/update/")
class Apikey_update(Resource):
    @identity.response(200, 'New APIKEY generated')
    def get(self):
        """
        Generate new APIKEY
        """
        return { "APIKEY": generate_APIKEY(check_identity())}, 200

@identity.response(500, 'Internal Server Error')
@identity.response(400, 'Missing parameter')
@identity.route("/masterkey/")
class Masterkey(Resource):

    @identity.response(200, 'APIKEY accepted')
    def get(self):
        """
        Generate temporary MASTER APIKEY
        """
        return { "MASTERKEY": generate_MASTERKEY(check_identity())}, 200

# @identity.response(500, 'Internal Server Error')
# @identity.response(400, 'Missing parameter')
# @identity.route("/masterkey/")
# class Masterkey(Resource):

#     @identity.response(200, 'APIKEY accepted')
#     def get(self):
#         """
#         Generate MASTER APIKEY
#         """
#         return { "MASTERKEY": generate_MASTERKEY({"masterkey": True}, True)}, 200
