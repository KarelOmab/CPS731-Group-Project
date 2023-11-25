import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import App
from classes.util.sqlservice import SqlService


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
    def test_challenge_usable_logged_out(self):
        response = self.test_client.get('/challenges/1')
        data = response.data.decode('utf-8')
        self.assertEqual(data.count("Sum"), 1)
        self.assertEqual(data.count("Difficulty: Easy"), 1)
        self.assertEqual(data.count(
            "Description: Write a function named sum that takes two integers a and b and returns their sum."), 1)
        self.assertEqual(data.count("Examples:"), 1)
        self.assertEqual(data.count("Comments"), 1)
        self.assertNotIn("Submissions", data)
        self.assertNotIn("Add a Comment", data)

    def test_challenge_usable_one_comment_logged_out(self):
        SqlService.insert_challenge_comment(2, 1, "test title", "test comment")
        response = self.test_client.get('/challenges/1')
        data = response.data.decode('utf-8')
        self.assertEqual(data.count("test title"), 1)
        self.assertEqual(data.count("test comment"), 1)
        self.assertEqual(data.count("Posted By:"), 1)
        self.delete_comments(1)

    def test_challenge_usable_multiple_comments_logged_out(self):
        SqlService.insert_challenge_comment(2, 1, "test title", "test comment")
        SqlService.insert_challenge_comment(
            2, 1, "test title2", "test comment2")
        response = self.test_client.get('/challenges/1')
        data = response.data.decode('utf-8')
        self.assertEqual(data.count("test title"), 1)
        self.assertEqual(data.count("test comment"), 1)
        self.assertEqual(data.count("test title2"), 1)
        self.assertEqual(data.count("test comment2"), 1)
        self.assertEqual(data.count("Posted By:"), 2)
        self.delete_comments(1)

    def test_challenge_usable_one_submission_logged_in(self):
        SqlService.insert_challenge_submission(1, 2, 1.0, len("test"), "test")
        self.test_client.post('/submit_login', data={
            "username": "test",
            "password": "test"
        })
        response = self.test_client.get('/challenges/1')
        data = response.data.decode('utf-8')
        self.assertEqual(data.count("Submitted At"), 1)
        self.assertEqual(data.count("Execution Time"), 1)
        self.assertEqual(data.count("Characters"), 1)
        self.assertEqual(data.count("1.0"), 1)
        self.assertEqual(data.count("4"), 1)
        self.delete_submissions(1, 2)
        self.logout()

    def test_challenge_usable_multiple_submissions_logged_in(self):
        SqlService.insert_challenge_submission(1, 2, 1.0, len("test"), "test")
        self.test_client.post('/submit_login', data={
            "username": "test",
            "password": "test"
        })
        SqlService.insert_challenge_submission(
            1, 2, 2.0, len("test1"), "test1")
        response = self.test_client.get('/challenges/1')
        data = response.data.decode('utf-8')
        self.assertEqual(data.count("Submitted At"), 1)
        self.assertEqual(data.count("Execution Time"), 1)
        self.assertEqual(data.count("Characters"), 1)
        self.assertEqual(data.count("1.0"), 1)
        self.assertEqual(data.count("2.0"), 1)
        self.assertEqual(data.count("4"), 1)
        self.assertEqual(data.count("5"), 1)
        self.delete_submissions(1, 2)
        self.logout()


if __name__ == '__main__':
    unittest.main()
