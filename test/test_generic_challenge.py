import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import App 



class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app_instance = App()
        self.test_client = self.app_instance.app.test_client()
        self.app_instance.app.testing = True
        # Other setup can go here

    def test_challenge_route_success(self):
        # Assume you have a challenge in your database with an id of 1
        response = self.test_client.get('/challenges/1')  # Use the test client to make a request

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTrue(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertIn('Sum', response.data.decode('utf-8'))  # Check for challenge title
        # Add more assertions for testcases, comments, and submissions as needed

    def test_challenge_route_failure(self):
        # Assume you have a challenge in your database with an id of 1
        response = self.test_client.get('/challenges/100')  # Use the test client to make a request

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check if the correct template was used
        self.assertFalse(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertNotIn('Sum', response.data.decode('utf-8'))  # Check for challenge title
        # Add more assertions for testcases, comments, and submissions as needed
