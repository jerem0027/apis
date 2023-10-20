#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity, generate_APIKEY, generate_MASTERKEY
from errors.errors import TokenError
from flask import request
from flask_restx import Resource, fields
from server.instance import server

api = server.api

identity_model = api.model('identity',{
    'name': fields.String(
        required=True,
        title='Name',
        example='Julien',
        description='Name of current guest',
    ),

    'id': fields.Integer(
        required=True,
        title='Unique ID',
        example=1,
        description='Unique ID'
    ),
})

identity = api.namespace(
    name='identity',
    description='Identity namespace'
)

@identity.response(500, 'Internal error')
@identity.route("/")
class Identity(Resource):
    @identity.response(200, 'Function ok')
    @identity.response(400, 'Missing parameter')
    def get(self):
        """
        check identity and access validity to API
        """
        return check_identity(), 200

    @identity.response(200, 'Function ok')
    @identity.response(400, 'Missing parameter')
    @identity.expect(identity_model)
    def post(self):
        """
        Generate APIKEY
        """
        if not "masterkey" in check_identity():
            raise TokenError("Access denied")
        return { "APIKEY": generate_APIKEY(request.json)}, 200

    @identity.response(200, 'Function ok')
    @identity.response(400, 'Missing parameter')
    def patch(self):
        """
        Generate MASTER APIKEY (only for admin)
        """
        return { "APIKEY": generate_MASTERKEY(check_identity())}, 200