from server import app


def test_logout():
    client = app.test_client()
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    # la redirection vers la page d'accueil (index).
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data
