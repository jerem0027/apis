#!/usr/bin/env python
# -*- coding: utf-8 -*-

from errors.errors import DBError
from server.envconfig import confdb
from server.instance import server

app, db = server.app, server.db

class User_DB(db.Model):
    __tablename__     = 'users'
    __bind_key__      = confdb.db_home_name
    pseudo            = db.Column(db.String(64), primary_key=True, unique=True)
    first_name        = db.Column(db.String(64), nullable=False)
    name              = db.Column(db.String(64), nullable=False)
    email             = db.Column(db.String(64), nullable=False)
    password          = db.Column(db.LargeBinary, nullable=False)
    birthdate         = db.Column(db.Date, nullable=False)
    inscription_date  = db.Column(db.Date, nullable=False)

    def check_pseudo(self) -> bool:
        """Return true if pseudo already exist"""
        return db.session.query(self.__class__).get(self.pseudo) != None
    
    def get_user(self):
        """Return User with this pseudo"""
        return db.session.query(self.__class__).get(self.pseudo)

    def add_user(self) -> bool:
        if self.check_pseudo():
            raise DBError(f"Error : User '{self.pseudo}' already exist")

        db.session.add(self)
        db.session.commit()
        return True

try:
    with app.app_context():
        db.create_all(bind_key=confdb.db_home_name)
except Exception as e:
    print(e)
    pass