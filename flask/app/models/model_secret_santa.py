#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restx import fields
from server.instance import server

api = server.api


form_user = api.model('user',{
    'first_name':  fields.String(
        required=True,
        title='Prenom',
        example='Zinedine',
        description='Prénom de la personne'
    ),

    'name': fields.String(
        required=False,
        title='Nom',
        description='Nom de la personne',
        example='Zidane',
    ),

    'username': fields.String(
        required=False,
        title='Pseudo',
        example='Log',
        description='Pseudo de la personne'
    ),

    'mail': fields.String(
        required=True,
        title='Email',
        example='jean_john@test.com',
        pattern="^[a-z][a-z0-9._]+@[a-z0-9_]+.[a-z]{2,3}$",
        description='Email de la personne'
    )
})


# Formulaire de demande
form_users = api.model('test-model',{
    'users':  fields.List(
        fields.Nested(form_user),
        required=True,
        title='List des personned participantes',
        description='The email address of the technical referent'
    )
})