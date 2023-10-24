#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.identity import check_identity
from core.utils import random_number
from errors.errors import DBError
from flask import request
from flask_restx import Resource
from server.instance import server

app, api, db = server.app, server.api, server.db

test_ns = api.namespace(
    name='tests',
    description='test namespace'
)

class Test(db.Model):
    __tablename__ = 'test'
    __bind_key__ = 'home_db'
    id = db.Column(db.Integer, primary_key=True, unique=True)

    def __init__(self):
        try:
            db.create_all(bind_key="test")
        except Exception as e:
            print(e)
            pass


    def add_test(id):
        new_test = Test(id=id)
        if not db.session.query(Test).get(new_test.id):
            db.session.add(new_test)
            db.session.commit()
        else:
            raise DBError("Un element avec la meme clé primaire existe déjà")

    def remove_test(id):
        old_test = db.session.query(Test).filter_by(id=id).first()
        if old_test:
            db.session.delete(old_test)
            db.session.commit()
        else:
            raise DBError("Aucun element avec cette clé primaire n'existe")

@test_ns.response(500, 'Internal Server Error')
@test_ns.route("/get_all")
class Random(Resource):
    @test_ns.response(200, 'Function ok')
    @test_ns.response(400, 'Missing parameter')
    def get(self):
        """
        test namespace
        """
        tests = Test.query.all()
        data = [test.id for test in tests]
        return {
            "status": "this is a test",
            "content": data
            }, 200

@test_ns.response(500, 'Internal Server Error')
@test_ns.route("/check_authentification")
class Random(Resource):
    @test_ns.response(200, 'Function ok')
    @test_ns.response(400, 'Missing parameter')
    def get(self):
        """
        test namespace
        """
        return check_identity()

@test_ns.response(500, 'Internal Server Error')
@test_ns.route("/manage/<string:id>")
class Random(Resource):
    @test_ns.response(200, 'Function ok')
    @test_ns.response(405, 'Key already exist')
    def put(self, id):
        """
        test namespace
        """
        Test.add_test(id)
        data = [test.id for test in Test.query.all()]
        return {
            "status": "this is a test",
            "content": data
            }, 200

    @test_ns.response(200, 'Function ok')
    @test_ns.response(405, 'Key not found')
    def delete(self, id):
        """
        test namespace
        """
        Test.remove_test(id)
        data = [test.id for test in Test.query.all()]
        return {
            "status": "this is a test",
            "content": data
            }, 200
    


@test_ns.response(500, 'Internal error')
@test_ns.route("/random/list_personne")
class Random(Resource):
    @test_ns.response(200, 'Function ok')
    @test_ns.response(400, 'Missing parameter')
    # @ns_random.expect(form_demande)
    def put(self):
        """
        Get list random
        """
        check_identity()    # check if user is in dataBase
        data = request.json

        if not "personnes" in data:
            return "Error parameter 'personnes' is missing.", 400

        while True:
            person_to_give = data["personnes"].copy()
            couple = []
            retry = 20
            for p in data["personnes"]:
                while retry > 0:
                    # generate random
                    i = random_number(len(person_to_give))
                    target = person_to_give[i]
                    if p != target:
                        couple.append((p, target))
                        person_to_give.remove(target)
                        break
                    retry -= 1
            if len(person_to_give) == 0:
                break
        return couple, 200