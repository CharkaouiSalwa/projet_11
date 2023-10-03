import json
import pytest
from server import app

# Charger les données JSON des clubs et des compétitions
with open('clubs.json', 'r') as clubs_file:
   clubs_data = json.load(clubs_file)

with open('competitions.json', 'r') as competitions_file:
   competitions_data = json.load(competitions_file)


def test_integration():
    # Accédez à la page d'accueil
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data

    # Soumettez le formulaire avec une adresse e-mail valide
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome' in response.data

    # Accédez à la page de réservation avec des valeurs de compétition et de club valides
    competition_name = 'Spring Festival'
    club_name = 'Simply Lift'
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert b'Book' in response.data

    #  Soumettez le formulaire de réservation avec le nombre de places requis
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': '1'
    })
    assert response.status_code == 200

    #  Accédez à la page d'affichage des points
    response = client.get('/points_display')
    assert response.status_code == 200
    assert b'Points Display Board' in response.data

    # Accédez à la page de déconnexion
    response = client.get('/logout')
    assert response.status_code == 302

if __name__ == '__main__':
    pytest.main()
