#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restx import fields
from server.instance import server

api = server.api

guest_model = api.model("guest",{
    "name": fields.String(
        required=True,
        title="Name",
        example="Julien",
        description="Name of current guest",
    ),

    "email": fields.String(
        required=True,
        title="Email",
        example="julien_mail@mail.com",
        description="Email of current guest"
    ),

    "target": fields.String(
        required=True,
        title="Target Name",
        example="Julien",
        description="Name of current guest target"
    ),

    "target_email": fields.String(
        required=True,
        title="Target Email",
        example="julien_mail@mail.com",
        description="Email of current guest target"
    )
})