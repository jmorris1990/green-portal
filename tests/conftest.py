import os

import pytest

from portal import create_app
from portal.db import get_db, init_db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DB_NAME': 'portal_test',
        'DB_USER': 'portal_user',
    })

    with app.app_context():
        init_db()

        with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
            con = get_db()
            cur = con.cursor()
            cur.execute(f.read())
            cur.close()
            con.commit()
            con.close()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# creating an object to put data into the database
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email=None, password=None):
        return self._client.post('/', data={'email': email, 'password': password})

    def login_teacher(self):
        return self.login(email='teacher@stevenscollege.edu', password='pbkdf2:sha256:150000$vabLpq6w$1b5021c0313f059dce39833e64ba44eba0dad10bdbd630f942469fc873781bb2') # qwerty hash

    # TODO: add login_student function
    def login_student(self):
        return self.login(email='student@stevenscollege.edu', password='pbkdf2:sha256:150000$ELq3TqsJ$1c60f43f7085a68425e165f27a74c7d7bcc94ce98e604b874e8419f7efefbc06') # asdfgh hash
    # TODO: add logout function
    def logout_student(self):
        return self._client.get('/')

    def logout_teacher(self):
        return self._client.get('/')

@pytest.fixture
def auth(client):
    return AuthActions(client)
