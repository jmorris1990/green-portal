from flask import session, g 
from portal import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form>' in response.data

# making a test for the login
def test_index(client, auth):
    assert client.get('/home.html').status_code == 200
    response = auth.login()
    assert response.headers['Locations'] == 'green-portal.herokuapp.com'

    with client:
        client.get('/')
        assert session['id'] == 1
        assert g.user['email'] == 'teacher@stevenscollege.edu'
