import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.util.sqlservice import SqlService
from app import App


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app_instance = App()
        self.test_client = self.app_instance.app.test_client()
        self.app_instance.app.testing = True

    def delete_comments(self, challenge_id):
        comments = SqlService.get_challenge_comments_by_id(challenge_id)
        for comment in comments:
            SqlService.purge_challenge_comment_by_id(comment.id)

    def delete_submissions(self, challenge_id, account_id):
        submissions = SqlService.get_challenge_submissions_by_id_and_account_id(
            challenge_id, account_id)

    def logout(self):
        # Logout of the session to avoid interfering with other tests
        self.app_instance.get("/logout")

    # all tests will use challenge with id 1
    # logged out tests
    def test_challenge_route_success(self):
        response = self.test_client.get('/challenges/1')
        print(response)
        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTrue(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertIn('Sum', response.data.decode(
            'utf-8'))  # Check for challenge title
        # Add more assertions for testcases, comments, and submissions as needed

if __name__ == '__main__':
    unittest.main()