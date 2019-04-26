from flask import session, g

def test_courses(client, auth):
    user = auth.login_student()
    response = client.get('/courses')
    assert response.status_code == 401

    user = auth.login_teacher()
    response = client.get('/courses')
    assert b'<ul class="courses">' in response.data
    assert b'<li>Course 1 <a href' in response.data
    assert b'<a href="/courses/add"' in response.data

def test_add_courses(client, auth):
    user = auth.login_student()
    response = client.get('/courses/add')
    assert response.status_code == 401 #Unauthorized

    user = auth.login_teacher()
    response = client.get('/courses/add')
    assert b'<form method="POST">' in response.data
    assert b'<label for="name">' in response.data
    assert b'<input type="text" name="name"' in response.data

    response = client.post('/courses/add', data=dict(name="New Course", code="EX 108", class_session="B", days="MWF", start="9:30:00", end="10:50:00", description="foo"))
    assert response.status_code == 302


def test_edit_courses(client, auth):
    user = auth.login_student()
    response = client.get('/courses/edit/1')
    assert response.status_code == 401

    user = auth.login_teacher()
    response = client.get('/courses/edit/1')
    assert b'<form method="POST"' in response.data
    assert b'<input type="text" name="name"' in response.data

    response = client.post('/courses/edit/1', data=dict(name="Edited Course", code="EX 170", class_session="A", days="TR", start="9:00:00", end="9:50:00", description="baz", id=1))
    assert response.status_code == 302

    response = client.get('/courses')
    assert b'<li>Edited Course' in response.data
