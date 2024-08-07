def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Please sign in" in response.data

def test_register_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login(client, app):
    with app.app_context():
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        assert response.status_code == 200
        # Additional assertions can be added here
