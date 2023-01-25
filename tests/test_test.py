from flask import Blueprint, render_template, request, url_for, flash,redirect
#from website.views.auth import login
import pytest
from website.models import User
from datetime import datetime
import json


@pytest.mark.registration
class TestReg:
    def test_registration(self, _db, client):
        data = {
            "firstName": "Konto testowe",
            "lastName": "aa",
            "email": "test@test.pl",
            "password": "123456789",
            "confirm_password": "123456789",
            "submit": "Sign Up"
        }
        response = client.post("/signup", method = "POST", data=data, follow_redirects=True)
        print(response.data)
        user = _db.session.query(User).filter(User.email == "test@test.pl").one_or_none()
        user.confirmed = True
        user.confirmed_on=datetime.now()
        _db.session.add(user)
        _db.session.commit()

        user = User.query.filter_by(email="test@test.pl").first()
        assert user is not None

    def test_registration2(self, _db, client):
        data = {
            "firstName": "Konto testowe2",
            "lastName": "aa2",
            "email": "test2@test.pl",
            "password": "123456789",
            "confirm_password": "123456789",
            "submit": "Sign Up"
        }
        response = client.post("/signup", method = "POST", data=data, follow_redirects=True)
        print(response.data)
        user = _db.session.query(User).filter(User.email == "test2@test.pl").one_or_none()
        user.confirmed = True
        user.confirmed_on=datetime.now()
        _db.session.add(user)
        _db.session.commit()

        user = User.query.filter_by(email="test2@test.pl").first()
        assert user is not None

    def test_registration3(self, _db, client):
        data = {
            "firstName": "",
            "lastName": "aa",
            "email": "",
            "password": "123456789",
            "confirm_password": "123456789",
            "submit": "Sign Up"
        }
        response = client.post("/signup", method = "POST", data=data, follow_redirects=True)
        print(response.data)
        user = _db.session.query(User).filter(User.email == "").one_or_none()
        assert user is None
        

    def test_login(self, client):
        data = {
            "email": "test@test.pl",
            "password": "123456789",
            "remember": "y",
            "submit": "Log In"
        }
        client.post("/login", method = "POST", data=data)
        response = client.get("/account", follow_redirects=True)
        #assert response.status_code == 200
        print(response.data)
        assert b"Konto testowe" in response.data




@pytest.mark.search
class TestSearch:
    def test_search(self, client):
        token = 111111111
        client.get("/search/token/" + str(token), query_string = {"length": 1})
        data = {
            "target": "ceneo",
            "product": "lalka",
            "amount": 1
        }
        client.get("/search/add/" + str(token), query_string=data)
        response = client.get("/search/" + str(token))
        print(response.data)
        assert b"Maileg" in response.data

    def test_search2(self, client):
        token = 111111112
        client.get("/search/token/" + str(token), query_string = {"length": 1})
        data = {
            "target": "ceneo",
            "product": "klocki",
            "amount": 1
        }
        client.get("/search/add/" + str(token), query_string=data)
        response = client.get("/search/" + str(token))
        print(response.data)
        assert b"Dromader Klocki Figurka" in response.data

    def test_search3(self, client):
        token = 111111113
        client.get("/search/token/" + str(token), query_string = {"length": 3})
        data = {
            "target": "ceneo",
            "product": "harry potter",
            "amount": 2
        }
        client.get("/search/add/" + str(token), query_string=data)
        data = {
            "target": "ceneo",
            "product": "kolorowanka",
            "amount": 40
        }
        client.get("/search/add/" + str(token), query_string=data)
        data = {
            "target": "ceneo",
            "product": "lego",
            "amount": 3
        }
        client.get("/search/add/" + str(token), query_string=data)
        response = client.get("/search/" + str(token))
        print(response.data)
        assert b"LEGO Nexo Knights" in response.data

    def test_search4(self, client):
        token = 111111114
        client.get("/search/token/" + str(token), query_string = {"length": 3})
        data = {
            "target": "allegro",
            "product": "harry potter",
            "amount": 2
        }
        client.get("/search/add/" + str(token), query_string=data)
        data = {
            "target": "allegro",
            "product": "kolorowanka",
            "amount": 40
        }
        client.get("/search/add/" + str(token), query_string=data)
        data = {
            "target": "allegro",
            "product": "lego",
            "amount": 3
        }
        client.get("/search/add/" + str(token), query_string=data)
        response = client.get("/search/" + str(token))
        print(response.data)
        assert b"Klocki Typu Lego Helikopter 3W1 Dla Dzieci" in response.data
        

