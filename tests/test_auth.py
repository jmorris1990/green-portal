from flask import session, g

def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login_teacher()
    print(response.data)
    assert response.status_code == 302


def test_flash_error(client, auth):
    response = client.post('/', data=dict(email='fake@email.com', password='fake'))
    assert b'<li class="message">Incorrect email</li>' in response.data

    response = client.post('/', data=dict(email='teacher@stevenscollege.edu', password='fake'))
    assert b'<li class="message">Incorrect password</li>' in response.data


def test_logout(client, auth):
    assert client.get('logout').status_code == 302
    response = auth.logout_student()
    assert response.status_code == 200

    with client:
        auth.logout_student()
        assert 'user' not in session
        auth.logout_teacher()
        assert 'user' not in session

def test_home(client, auth):
    response = client.get('/home')
    assert response.status_code == 302

    user = auth.login_teacher()
    response = client.get('/home')
    print(response.data)
    assert b'<h1>Welcome to the Portal</h1>' in response.data

    user = auth.login_student()
    response = client.get('/home')
    assert b'<h1>Welcome to the Portal</h1>' in response.data
