#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.datastructures import FileStorage
from flask_restx import fields
from server.instance import server

api = server.api

# Upload DAT file
upload_file = api.parser()
upload_file.add_argument('file', location='files', type=FileStorage, required=True)
doc_file = {"file": "Documentation fichier (peut contenir de l'HTML)"}


form_personne = api.model('personne',{
    'prenom':  fields.String(
        required=True,
        title='Prenom',
        example='Zinedine',
        description='Prénom de la personne'
    ),

    'nom': fields.String(
        required=False,
        title='Nom',
        description='Nom de la personne',
        example='Zidane',
    ),

    'pseudo': fields.String(
        required=False,
        title='Pseudo',
        example='Log',
        description='Pseudo de la personne'
    ),

    'email': fields.String(
        required=True,
        title='Email',
        example='jean_john@test.com',
        pattern="^[a-z][a-z0-9._]+@[a-z0-9_]+.[a-z]{2,3}$",
        description='Email de la personne'
    )
})



# Formulaire de demande
form_demande = api.model('test-model',{
    'personnes':  fields.List(
        fields.Nested(form_personne),
        required=True,
        title='List des personned participantes',
        description='The email address of the technical referent'
    )
})