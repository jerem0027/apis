#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity, generate_APIKEY, generate_MASTERKEY
from errors.errors import TokenError
from flask_restx import Resource, fields
from server.instance import server

from flask import request

api = server.api

identity_model = api.model('identity',{
    'pseudo': fields.Integer(
        required=True,
        title='Pseudo',
        example=1,
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
    @identity.response(200, 'Function ok')
    def get(self):
        """
        check identity and access validity to API
        """
        return check_identity(), 200

    @identity.response(200, 'Function ok')
    @identity.expect(identity_model)
    def post(self):
        """
        Generate APIKEY
        """
        if not "masterkey" in check_identity():
            raise TokenError("Access denied")
        return { "APIKEY": generate_APIKEY(request.json)}, 200

    @identity.response(200, 'Function ok')
    def patch(self):
        """
        Generate MASTER APIKEY (only for admin)
        """
        return { "APIKEY": generate_MASTERKEY(check_identity())}, 200