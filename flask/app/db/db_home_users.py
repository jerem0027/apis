#!/usr/bin/env python
# -*- coding: utf-8 -*-

from errors.errors import DBError, ObjectNotFound
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

    def __str__(self) -> str:
        return f"{self.pseudo} - {self.first_name} - {self.name} - {self.email} - {self.birthdate} - {self.inscription_date}"

    def to_dict(self) -> dict:
        return {
            "pseudo" : self.pseudo,
            "first_name" : self.first_name,
            "name" : self.name,
            "email" : self.email,
            "birthdate" : str(self.birthdate),
            "inscription_date" : str(self.inscription_date)
        }

    def check_pseudo(self) -> bool:
        """Return true if pseudo already exist"""
        try:
            user = db.session.query(self.__class__).get(self.pseudo)
        except:
            raise DBError("Error during update of user")
        return user != None

    def get(self) -> dict:
        """Return User with this pseudo"""
        try:
            user = db.session.query(self.__class__).get(self.pseudo)
        except:
            raise DBError("Error during update of user")
        return user.to_dict()

    def create(self) -> None:
        if self.check_pseudo():
            raise DBError(f"Error : User '{self.pseudo}' already exist")
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise DBError("Error during update of user")

    def delete(self) -> None:
        if not self.check_pseudo():
            raise ObjectNotFound(f"Error : User '{self.pseudo}' not found")

        try:
            db.session.delete(self.get_user())
            db.session.commit()
        except:
            raise DBError("Error during update of user")

    def update(self) -> None:
        if not self.check_pseudo():
            raise ObjectNotFound(f"Error : User '{self.pseudo}' not found")
        user = self.get_user()
        for key in list(self.__dict__. keys())[1:]:
            if key == "pseudo" or getattr(self, key) == None:
                continue
            if getattr(self, key) != getattr(user, key):
                setattr(user, key, getattr(self, key))
        try:
            db.session.add(user)
            db.session.commit()
        except:
            raise DBError("Error during update of user")

try:
    with app.app_context():
        db.create_all(bind_key=confdb.db_home_name)
except Exception as e:
    print(e)
    pass