import json
from flask import Flask
import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data

def test_show_summary_valid(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_show_summary_invalid(client):
    response = client.post('/showSummary', data={'email': 'nonexistent@example.com'})
    assert response.status_code == 302

def test_book_valid(client):
    competition_name = 'Spring Festival'
    club_name = 'Simply Lift'
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert b'Book' in response.data

def test_purchase_places_valid(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '5'})
    assert response.status_code == 302

def test_purchase_places_invalid_club_or_competition(client):
    competition_name = 'Spring Festival'
    club_name = 'NonExistentClub'
    response = client.post('/purchasePlaces', data={'club': club_name, 'competition': competition_name, 'places': '5'})
    assert response.status_code == 200

def test_purchase_places_not_enough_places(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '50'})
    assert response.status_code == 200

def test_purchase_places_not_enough_points(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '20'})
    assert response.status_code == 200

def test_points_display(client):
    response = client.get('/points_display')
    assert response.status_code == 200
    assert b'Points Display Board' in response.data

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302

if __name__ == '__main__':
    pytest.main()
