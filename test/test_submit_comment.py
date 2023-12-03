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
        if comments:
            for comment in comments:
                SqlService.purge_challenge_comment_by_id(comment.id)

    def delete_submissions(self, challenge_id, account_id):
        submissions = SqlService.get_challenge_submissions_by_id_and_account_id(
            challenge_id, account_id)
        if submissions:
            for submission in submissions:
                SqlService.purge_challenge_submission_by_id(submission.id)

    def test_empty_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_single_alpha_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "a",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_single_numeric_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "1",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_single_special_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "@",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_alpha_ascending_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "ab",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_alpha_descending_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "ba",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_alpha_random_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "acb",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_numeric_ascending_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "12",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_numeric_descending_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "21",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_numeric_random_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "132",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count(
                "Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_special_ascending_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "!@",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_special_descending_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "@!",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_multi_special_random_empty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "!#@",
                "commentText": ""
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_single_alpha(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "",
                "commentText": "a"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_single_numeric(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "",
                "commentText": "1"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_single_special(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "",
                "commentText": "@"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_alpha_ascending(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle": "",
                "commentText": "ab"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_alpha_descending(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "ba"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_alpha_random(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "acb"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_numeric_ascending(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "12"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_numeric_descending(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "21"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_numeric_random(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "132"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_special_ascending(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "!@"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_special_descending(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "@!"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_empty_multi_special_random(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"",
                "commentText": "!#@"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("Please provide a title and text for your comment"), 1)
            self.assertNotIn("commented on", data)
            self.delete_comments(1)
    
    def test_nonempty_nonempty(self):
        with self.test_client.session_transaction() as session:
            session["username"]= "test"
            session["password"]= "test"
            session["privileged_mode"] = False
            response = self.test_client.post('/submit_comment/1', data={
                "commentTitle":"abcd",
                "commentText": "efgh"
            }, follow_redirects=True)
            data = response.data.decode('utf-8')
            self.assertEqual(data.count("abcd"), 1)
            self.assertEqual(data.count("efgh"), 1)
            self.assertEqual(data.count("commented on"), 1)
            self.assertNotIn("Please provide a title and text for your comment", data)
            self.delete_comments(1)

if __name__ == '__main__':
    unittest.main()
