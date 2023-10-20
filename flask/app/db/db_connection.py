#!/usr/bin/env python
# -*- coding: utf-8 -*-

from errors.errors import DBError
from server.envconfig import confdb
from server.instance import server

app, db = server.app, server.db

class APIKEY(db.Model):
    __bind_key__ = confdb.db_home_name
    __tablename__ = "apikey"
    key = db.Column(db.String(64), primary_key=True)

    def __init__(self, key):
        self.key = key

    def add_apikey(self) -> None:
        if not db.session.query(APIKEY).get(self.id):
            db.session.add(self)
            db.session.commit()
        else:
            raise DBError("Un element avec la meme clé primaire existe déjà") # Pas censé arriver

    def check_apikey(self) -> bool:
        data = self.query.filter_by(key=self.key).first()
        return data != None

try:
    with app.app_context():
        db.create_all(bind_key=confdb.db_home_name)
except Exception as e:
    print(e)
    pass
