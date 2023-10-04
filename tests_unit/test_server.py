import unittest
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the GUDLFT Registration Portal!', response.data)

    def test_mail_valid(self):
        response = self.app.post('/showSummary', data={'email': 'john@simplylift.co'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_mail_invalid(self):
        response = self.app.post('/showSummary', data={'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 302)

    def test_book_valid(self):
        competition_name = 'Spring Festival'
        club_name = 'Simply Lift'
        response = self.app.get(f'/book/{competition_name}/{club_name}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book', response.data)


    def test_purchase_places_valid(self):
        response = self.app.post('/purchasePlaces',
                                    data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '5'})
        self.assertEqual(response.status_code, 200)

    def test_purchase_places_invalid_club_or_competition(self):
        competition_name = 'Spring Festival'
        club_name = 'NonExistentClub'
        response = self.app.post('/purchasePlaces', data={'club': club_name, 'competition': competition_name, 'places': '5'})
        self.assertEqual(response.status_code, 200)



    def test_purchase_places_not_enough_places(self):
        response = self.app.post('/purchasePlaces',
                                    data={'club': 'Simply Lift', 'competition': 'Spring Festival',
                                        'places': '50'})
        self.assertEqual(response.status_code, 200)



    def test_purchase_places_not_enough_points(self):
        response = self.app.post('/purchasePlaces',
                                    data={'club': 'Simply Lift', 'competition': 'Spring Festival',
                                        'places': '20'})
        self.assertEqual(response.status_code, 200)

    def test_points_display(self):
        response = self.app.get('/points_display')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Points Display Board', response.data)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
