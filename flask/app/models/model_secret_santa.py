#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restx import fields
from server.instance import server

api = server.api


form_guest = api.model("user",{
    "name": fields.String(
        required=True,
        title="Nom",
        description="Nom/Prenom du guest",
        example="Peter P.",
    ),
    "email": fields.String(
        required=True,
        title="Email",
        example="peter_parker@gmail.com",
        pattern="^[a-z][a-z0-9._]+@[a-z0-9_]+.[a-z]{2,3}$",
        description="Email du guest"
    )
})

# Formulaire de demande
form_secret_santa = api.model("form_secret_santa",{
    "title": fields.String(
        required=False,
        title="Title",
        description="Titre du secret santa",
        example="Secret santa des champions",
    ),
    "date_end": fields.Date(
        required=True,
        title="Date end",
        example="25-12-2023",
        description="Date fin prévu du secret santa"
    ),
    "guests":  fields.List(
        fields.Nested(form_guest),
        required=True,
        min_items=3,
        title="List des personnes participantes",
        description="The email address of the technical referent"
    )
})

form_update_secret_santa = api.model("form_update_secret_santa",{
    "title": fields.String(
        required=False,
        title="Title",
        description="Nouveau titre du secret santa",
        example="Secret santa des champions",
    ),
    "date_end": fields.Date(
        required=False,
        title="Date end",
        example="25-12-2023",
        description="Nouvelle date fin prévu du secret santa"
    )
})

form_update_guest_gift = api.model("form_update_guest_gift",{
    "gift_list":  fields.List(
        fields.String(
            required=True,
            title="Cadeau",
            description="Une idée de cadeau",
            example="Cartes Pokémon"
        ),
        required=True,
        max_items=5,
        title="Liste cadeaux",
        description="Liste d'idée cadeau"
    )
})