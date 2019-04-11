from flask import session, g
from portal import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data

def test_home(client, auth):
    response = client.get('/home')
    assert response.status_code == 302

    user = auth.login_teacher()
    response = client.get('/home')
    print(response)
    assert b'<h1>Welcome to the Portal</h1>' in response.data

    user = auth.login_student()
    response = client.get('/home')
    assert b'<h1>Welcome to the Portal</h1>' in response.data
