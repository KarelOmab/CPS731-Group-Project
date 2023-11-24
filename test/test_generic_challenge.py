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
    def test_challenge_usable_logged_out(self):
        response = self.test_client.get('/challenges/1')
        data=response.data.decode('utf-8')
        self.assertIn("Sum", data)
        self.assertIn("Difficulty: Easy", data)
        self.assertIn("Description: Write a function named sum that takes two integers a and b and returns their sum.", data)
        self.assertIn("Examples:", data)
        self.assertIn("Comments", data)
        self.assertNotIn("Submissions", data)
        self.assertNotIn("Add a Comment", data)
    
    def test_challenge_usable_one_comment_logged_out(self):
        SqlService.insert_challenge_comment(2, 1, "test title", "test comment")
        response = self.test_client.get('/challenges/1')
        data=response.data.decode('utf-8')
        self.assertIn("test title", data)
        self.assertIn("test comment", data)
        self.assertIn("Posted By:", data)
        self.delete_comments(1)

if __name__ == '__main__':
    unittest.main()