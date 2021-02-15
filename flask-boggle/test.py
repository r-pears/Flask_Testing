from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Before every test we want to do these things."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Testing to see that all the relevant information is shown on the homepage."""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('timesplayed'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test the validity of words in a session."""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"]]
        response = self.client.get('/check-word?word=dog')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=invalid')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=invalid')
        self.assertEqual(response.json['result'], 'not-word')
