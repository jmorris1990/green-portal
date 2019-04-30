def test_enter_grade(client, auth):
    user = auth.login_teacher()
    response = client.get('/sessions/1/assignments/1/submissions/1/update')

    assert b'<form method="POST"' in response.data
    assert b'<input type="number"' in response.data

    response = client.post('/sessions/1/assignments/1/submissions/1/update', data=dict(grade="100"))

    assert response.status_code == 302

    user = auth.login_student()
    response = client.get('/sessions/1/assignments/1/submissions/1/update')
    assert response.status_code == 401

def test_submissions(client, auth):
    user = auth.login_student()
    response = client.get('/sessions/1/assignments/1/submissions')
    assert response.status_code == 200

    user = auth.login_teacher()
    response = client.get('/sessions/1/assignments/1/submissions')
    assert b'<ul' in response.data
