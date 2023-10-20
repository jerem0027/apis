#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import ssl

from core.identity import check_identity
from flask import request
from flask_restx import Resource
from server.envconfig import configMail
from server.instance import server

app, api, db = server.app, server.api, server.db

ns = api.namespace(
    name='email',
    description='Send an email'
)

@ns.response(500, 'Internal error')
@ns.route("/send_mail/<string:email>")
class unique_demande(Resource):
    @ns.response(200, 'Email send')
    @ns.response(400, 'Error during email sent')
    def post(self, email):
        """
        Send an email.
        """
        check_identity()    # check if user is in dataBase
        message = request.data.get('message', None)

        context = ssl.create_default_context()
        with smtplib.SMTP(configMail.SMTP_SERVER, configMail.MAIL_PORT) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(configMail.SENDER_EMAIL, configMail.PASSWORD)
            server.sendmail(configMail.SENDER_EMAIL, email, message.encode('utf-8'))
            print("email envoyé à " + email)

        return "Success", 200