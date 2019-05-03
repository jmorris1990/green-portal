def test_assignments(client, auth):
    user = auth.login_teacher()
    response = client.get('sessions/1/assignments')

    assert b'<ul' in response.data
    assert b'<li class="assignmentspacing">' in response.data
    assert b'<span>Assignment 1</span>' in response.data
    assert b'<p>This is assignment 1</p>' in response.data

def test_create_assignments(client, auth):
    user = auth.login_teacher()

    response = client.get('sessions/1/assignments/create')
    assert b'<form method="POST"' in response.data


    response = client.post('sessions/0/assignments/create', data=dict(name='New Assignment', description='This is a new assignment.', total_points='100'))
    assert b'<form method="POST"' in response.data

    response = client.post('sessions/1/assignments/create', data=dict(name='New Assignment', description='This is a new assignment.', total_points='100'))
    assert response.status_code == 302

    response = client.get('sessions/1/assignments')
    assert b'<ul' in response.data
    assert b'<li class="assignmentspacing">' in response.data
    assert b'<span>New Assignment</span>' in response.data
    assert b'<p>This is a new assignment.</p>' in response.data

    user = auth.login_student()
    response = client.get('sessions/1/assignments/create')
    assert response.status_code == 401
