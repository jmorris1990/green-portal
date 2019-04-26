from flask import g, session

def test_sessions(client, auth):
    user = auth.login_student()
    response = client.get('/sessions')

    assert b'<ul' in response.data
    print(response.data)
    assert b'<li>Course 1 CSET 180 A MTWRF 12:00:00-16:30:00' in response.data
    assert b'<li>Course 1 CSET 180 C MWF 12:00:00-13:00:00' not in response.data

def test_add_session(client, auth):
    user = auth.login_teacher()
    response = client.get('/sessions/add')
    assert response.status_code == 200

    response = client.post('/sessions/add', data=dict(course_id="1", session_name="B", day="MWF", start_time="12:00", end_time="14:00", student1="1"))
    assert response.status_code == 302

    response = client.post('/sessions/add', data=dict(course_id="0", session_name="B", day="MWF", start_time="12:00", end_time="14:00", student1="1"))
    assert b'<form method="POST"' in response.data

    user = auth.login_student()
    response = client.get('/sessions/add')
    assert response.status_code == 401
