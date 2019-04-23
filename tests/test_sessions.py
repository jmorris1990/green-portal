from flask import g, session

def test_sessions(client, auth):
    user = auth.login_student()
    response = client.get('/sessions')

    assert b'<ul' in response.data
    print(response.data)
    assert b'<li>Course 1 CSET 180 A MTWRF 12:00:00-16:30:00' in response.data
    assert b'<li>Course 1 CSET 180 C MWF 12:00:00-13:00:00' not in response.data
