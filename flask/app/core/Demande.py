#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from errors.errors import DBError
from server.envconfig import DEBUG
from server.instance import server

db = server.db

class DataBase():

    def __init__(self, data):
        self.prenom = data["prenom"]
        self.nom = data["nom"]
        self.email = data["email"]
        self.pseudo = data["pseudo"]

    def update_in_db(self):
        demande = dbInvite.query.filter(dbInvite.id == self.id).first()
        demande.id_care = self.id_care
        db.session.commit()

    def insert_in_db(self):

        # Check if tenant_name is not already use
        if not DEBUG and dbInvite.query.filter(dbInvite.nom_technique_tenant == self.tenant_name).count() > 0:
            raise DBError("This tenant name is still use !")

        for i in range(len(self.env_PRD),9):
            self.env_PRD.append(None)
        for i in range(len(self.env_noPRD),9):
            self.env_noPRD.append(None)

        data = dbInvite(
                prenom = self.prenom,
                nom = self.nom,
                email = self.email,
                pseudo = self.pseudo,
        )
        try:
            db.create_all() # Creation de la base de donnée selon le Model "dbInvite"
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(e)
            if db.session.rollback():
                logging.error("Une erreur est survenue lors de l'insertion en db")
                raise DBError("ne erreur est survenue lors de l'insertion en db")




class dbInvite(db.Model):
    __tablename__ = 'Invite'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String)
    nom = db.Column(db.String)
    email = db.Column(db.String)
    pseudo = db.Column(db.String)

    def __repr__(self):
        return '<Invite %r>' % self

    def affiche_dbInvite(self):
        """
        Affichage des ligne de la base de données
        """
        return {
            "id" : self.id,
            "prenom" : self.prenom,
            "nom" : self.nom,
            "email" : self.email,
            "pseudo" : self.pseudo,
        }

# def remove_from_db(public_id):
#     demande = dbInvite.query.filter(dbInvite.public_id == public_id).one()
#     db.session.delete(demande)
#     db.session.commit()