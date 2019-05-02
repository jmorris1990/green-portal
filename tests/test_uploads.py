def test_upload(client, auth):
    user = auth.login_teacher()
    response = client.get('/upload/1')
    assert response.status_code == 401

    user = auth.login_student()
    response = client.get('/upload/1')
    assert response.status_code == 200

    response = client.post('/upload/1')
    assert response.status_code == 302

