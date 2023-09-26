import pytest
from server import app
import json

# Charger les données JSON des clubs et des compétitions
with open('clubs.json', 'r') as clubs_file:
   clubs_data = json.load(clubs_file)

with open('competitions.json', 'r') as competitions_file:
   competitions_data = json.load(competitions_file)




def test_purchase_places_max_places_exceeded():
   client = app.test_client()
   comp = competitions_data["competitions"][1]
   club = clubs_data["clubs"][0]
   response = client.post('/purchasePlaces', data={
       "club": club['name'],
       "competition": comp['name'],
       "places": 13
   })
   assert "You can only book up to 12 places." in response.data.decode()
   assert response.status_code == 200

def test_purchase_places_not_enough_points():
   client = app.test_client()
   comp = competitions_data["competitions"][1]
   club = clubs_data["clubs"][1]
   response = client.post('/purchasePlaces', data={
       "club": club['name'],
       "competition": comp['name'],
       "places": 6
   })
   assert "Not enough points to make the booking." in response.data.decode()
   assert response.status_code == 200



def test_purchase_places_successful_booking():
   client = app.test_client()
   comp = competitions_data["competitions"][1]
   club = clubs_data["clubs"][0]
   response = client.post('/purchasePlaces', data={
       "club": club['name'],
       "competition": comp['name'],
       "places": 1
   }, follow_redirects=True)

   assert response.status_code == 200

