def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login_teacher()
    assert response.status_code == 200
    print(response.headers)
    print(response.data)
    
    # with client:
    #     client.get('/')
    #     assert session['id'] == 1
    #     assert g.user['email'] == 'teacher@stevenscollege.edu'
