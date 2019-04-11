def test_courses(client, auth):
    user = auth.login_student()
    response = client.get('/courses')
    assert b'<ul class="courses">' in response.data
    assert b'<li>Course 1</li>' in response.data

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

def test_edit_courses(client, auth):
    user = auth.login_student()
    response = client.get('/courses/edit/1')
    assert response.status_code == 404

    user = auth.login_teacher()
    response = client.get('/courses/edit/1')
    assert b'<form method="POST">' in response.data
    assert b'<label for="name">' not in response.data
    assert b'<input type="text" name="name"' not in response.data
    assert b'<label for="time">' in response.data
    assert b'<input type="text" name="time"' in response.data
