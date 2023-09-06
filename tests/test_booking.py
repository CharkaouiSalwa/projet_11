import pytest
from server import app, competitions, clubs  # Importez les modules appropriés depuis votre application
from datetime import datetime, timedelta
import json

date_past = datetime.now() - timedelta(days=7)  # Date d'une semaine passée
date_future = datetime.now() + timedelta(days=7)  # Date d'une semaine à venir

# une compétition passée et un club valide
competition_name = "Spring Festival"
club_name = "Simply Lift"

# Test de la fonction book pour un cas où le booking réussit (compétition passée)
def test_successful_booking_past():
    client = app.test_client()
    # Recherchez la compétition correspondante par son nom
    found_competition = next((c for c in competitions if c['name'] == competition_name), None)

    if found_competition and datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < date_past:
        response = client.get(f'/book/{competition_name}/{club_name}')
        assert response.status_code == 200
        assert b'book' in response.data

# Test de la fonction book pour un cas où le booking échoue (compétition future)
def test_failed_booking_future():
    client = app.test_client()
    # Recherchez la compétition correspondante par son nom
    found_competition = next((c for c in competitions if c['name'] == competition_name), None)

    if found_competition and datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') >= date_past:
        response = client.get(f'/book/{competition_name}/{club_name}')
        assert response.status_code == 200
        assert b'Error message for future competition' in response.data

