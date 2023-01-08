from flask import Blueprint, render_template, request, url_for, flash,redirect
#from website.views.auth import login
import pytest


@pytest.mark.web
def test_login(client):
    data = {
        "email": "tnl89130@nezid.com",
        "password": "123456789",
        "remember": "y",
        "submit": "Log In"
    }
    client.post("/login", method = "POST", data=data)
    response = client.get("/account", follow_redirects=True)
    #assert response.status_code == 200
    print(response.data)
    assert b"Jakub" in response.data
    