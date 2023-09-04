from server import app

# Testez la fonction showSummary() avec un e-mail valide
def test_showSummary_with_valid_email():
    client = app.test_client()
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Testez la fonction showSummary() avec un e-mail invalide
def test_showSummary_with_invalid_email():
    client = app.test_client()
    response = client.post('/showSummary', data={'email': 'invalid_email@example.com'})
    assert response.status_code == 302  # Vérifiez que la réponse est une redirection (code 302)

