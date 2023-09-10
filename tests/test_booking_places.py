import pytest
from server import app
from datetime import datetime




# une compétition passée et un club valide
competition_name = "Spring Festival"
club_name = "Simply Lift"


# Test de la fonction book pour un cas où le booking réussit (compétition passée)
def test_successful_booking_past():
    client = app.test_client()
    competition_date = datetime.strptime("2022-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert b'book' in response.data



