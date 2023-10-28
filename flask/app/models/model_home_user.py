#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restx import fields
from server.instance import server

api = server.api

model_home_user_password = api.model('model_home_user_password',{
    'password': fields.String(
        required=True,
        title='password',
        example='azerty123',
        description='Password of user',
    )
})

model_home_user_connection = api.model('home_user_connection',{
    'pseudo': fields.String(
        required=True,
        title='Pseudo',
        example='dark_lord',
        description='Pseudo of user',
        pattern="^[a-z][-a-z0-9_]+[a-z0-9]$"
    ),

    'password': fields.String(
        required=True,
        title='password',
        example='azerty123',
        description='Password of user',
    )
})

model_home_user = api.model('home_user',{

    'pseudo': fields.String(
        required=True,
        title='Pseudo',
        example='dark_lord',
        description='Pseudo of new user',
        pattern="^[a-z][-a-z0-9_]+[a-z0-9]$"
    ),

    'first_name': fields.String(
        required=True,
        title='First_name',
        example='Julien',
        description='First name of new user',
        pattern="^[a-zA-z][a-z- ]+[a-z]$"
    ),

    'birthdate': fields.Date(
        required=True,
        title='Birthdate',
        example='01-01-2023',
        description='Birthdate of the new user'
    ),

    'name': fields.String(
        required=True,
        title='Name',
        example='Dupont',
        description='Name of new user',
        pattern="^[a-zA-z][a-z- ]+[a-z]$"
    ),

    'email': fields.String(
        required=True,
        title='Email',
        example='julien_dupont@mail.com',
        description='Email of new user',
        pattern="^[a-z][-a-z_0-9.]+@[a-z-.]+$"
    ),

    'password': fields.String(
        required=True,
        title='password',
        example='azerty123',
        description='Password of new user',
    )
})