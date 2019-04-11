from flask import session

def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login_teacher()
    assert response.status_code == 200
    print(response.headers)
    print(response.data)

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
