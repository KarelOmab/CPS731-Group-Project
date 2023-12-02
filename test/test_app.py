import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the parent directory to the PYTHONPATH so the App class can be imported
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import App
from classes.account.user import User
from classes.challenge.challenge import Challenge
from classes.challenge.challengetest import ChallengeTest

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        #Set up a test client before each test
        app = App().app
        app.testing = True
        self.client = app.test_client()

        # Instantiate Challenge and ChallengeTest objects
        self.challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Some Challenge Name",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="foo",
            stub_block="# TODO",
            time_allowed_sec=5
        )

        self.challenge_test = ChallengeTest(
            id=1,
            challenge_id=1,
            is_deleted=False,
            test_input="6, 12",
            test_output="18"
        )

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    @patch('classes.util.sqlservice.SqlService.insert_account')
    def test_successful_registration(self, mock_insert):
        mock_insert.return_value = [{'message': 'Success'}]
        response = self.client.post('/submit_registration', data={
            'username': 'testuser',
            'password': 'password123',
            'email_address': 'test@test.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful', response.get_data(as_text=True))

    def test_missing_fields(self):
        response = self.client.post('/submit_registration', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please fill all fields', response.get_data(as_text=True))

    @patch('classes.util.sqlservice.SqlService.insert_account')
    def test_username_in_use(self, mock_insert):
        mock_insert.return_value = [{'message': 'Username in use'}]
        response = self.client.post('/submit_registration', data={
            'username': 'existinguser',
            'password': 'password123',
            'email_address': 'test@test.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already in use', response.get_data(as_text=True))

    @patch('classes.util.sqlservice.SqlService.insert_account')
    def test_email_in_use(self, mock_insert):
        mock_insert.return_value = [{'message': 'Email in use'}]
        response = self.client.post('/submit_registration', data={
            'username': 'testuser',
            'password': 'password123',
            'email_address': 'existing@test.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email already in use', response.get_data(as_text=True))

    @patch('classes.util.sqlservice.SqlService.insert_account')
    def test_exception_during_registration(self, mock_insert):
        mock_insert.side_effect = Exception
        response = self.client.post('/submit_registration', data={
            'username': 'testuser',
            'password': 'password123',
            'email_address': 'test@test.com'
        })
        self.assertEqual(response.status_code, 500)

    def test_non_post_request(self):
        response = self.client.get('/submit_registration')
        self.assertEqual(response.status_code, 405)

    @patch('classes.util.cryptoservice.CryptoService.hash_password')
    @patch('classes.util.sqlservice.SqlService.get_account_by_username_password')
    def test_successful_login(self, get_account, mock_hash_password):
        mock_hash_password.return_value = 'hashed_password'
        get_account.return_value = User(id=1, username='testuser')
        response = self.client.post('/submit_login', data={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/' in response.location)

    def test_missing_credentials(self):
        response = self.client.post('/submit_login', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter both username and password', response.get_data(as_text=True))

    @patch('classes.util.cryptoservice.CryptoService.hash_password')
    @patch('classes.util.sqlservice.SqlService.get_account_by_username_password')
    def test_invalid_credentials(self, get_account, mock_hash_password):
        mock_hash_password.return_value = 'hashed_password'
        get_account.return_value = None
        response = self.client.post('/submit_login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password', response.get_data(as_text=True))

    @patch('classes.util.sqlservice.SqlService.get_account_by_username_password', side_effect=Exception)
    def test_exception_during_login(self, _):
        response = self.client.post('/submit_login', data={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('An error occurred during login - please try again later', response.get_data(as_text=True))

    def test_logout(self):
        # Set up a mock session
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['username'] = 'testuser'
                sess['privileged_mode'] = False

            # Call the logout method
            response = c.get('/logout')

            # Assert the session is cleared
            with c.session_transaction() as sess:
                self.assertNotIn('user_id', sess)
                self.assertNotIn('username', sess)
                self.assertNotIn('privileged_mode', sess)

            # Assert the user is redirected to the index page
            self.assertEqual(response.status_code, 302)
            self.assertTrue('/' in response.location)

    def test_login_page(self):
        response = self.client.get('/login')

        # Check if the response is OK and the correct template is being rendered
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    
    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.dockerservice.DockerService.validate_user_method')
    @patch('classes.util.sqlservice.SqlService.insert_challenge_submission')
    def test_submission_route_post_method_with_valid_data(self, mock_insert_submission, mock_validate_user_method, mock_get_challenge_tests_by_id, mock_get_challenge_by_id):
        mock_insert_submission.return_value = True  # Mock successful submission insertion
        mock_validate_user_method.return_value = (True, "valid")
        mock_get_challenge_by_id.return_value = self.challenge
        mock_get_challenge_tests_by_id.return_value = [self.challenge_test]

        with self.client.session_transaction() as session:
            session['user_id'] = 'some_user_id'  # Set user ID in session

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)

        self.assertEqual(response.status_code, 200)

    def test_submission_non_post_method(self):
        response = self.client.get('/submission/1')
        self.assertEqual(response.status_code, 405)

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    def test_submission_no_challenge_found(self, mock_get_challenge_by_id):
        mock_get_challenge_by_id.return_value = None
        response = self.client.post('/submission/1', data={'stub-block': 'code'})
        self.assertEqual(response.status_code, 404)

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    def test_submission_no_tests_implemented(self, mock_get_tests, mock_get_challenge):
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = None
        response = self.client.post('/submission/1', data={'stub-block': 'code'})
        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.json, {
            "message": "System error: Test Cases Not Implemented. Please come back later!",
            "flash": {"message": "Test cases are not implemented yet.", "category": "error"}
        })

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.dockerservice.DockerService.validate_user_method')
    def test_submission_invalid_stub(self, mock_validate, mock_get_tests, mock_get_challenge):
        mock_validate.return_value = (False, "Invalid stub")
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]
        response = self.client.post('/submission/1', data={'stub-block': 'invalid code'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "message": False,
            "flash": {"message": "Invalid stub", "category": "error"}
        })

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.sqlservice.SqlService.insert_challenge_submission')
    def test_submission_database_insertion_failure(self, mock_insert, mock_get_tests, mock_get_challenge):
        mock_insert.return_value = False
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]
        response = self.client.post('/submission/1', data={'stub-block': 'valid code'})
        self.assertEqual(response.status_code, 400)

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.sqlservice.SqlService.insert_challenge_submission')
    def test_submission_exception_handling(self, mock_insert_submission, mock_get_challenge_tests_by_id, mock_get_challenge_by_id):
        mock_get_challenge_by_id.return_value = self.challenge
        mock_get_challenge_tests_by_id.return_value = [self.challenge_test]
        
        # Mock insert_challenge_submission to raise an exception
        mock_insert_submission.side_effect = Exception("Test Exception")

        with self.client.session_transaction() as session:
            session['user_id'] = 'test_user_id'  # Set user ID in session

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("An unexpected error occurred: Test Exception", response.json.get("flash", {}).get("message", ""))
        self.assertIn("Test Exception", response.json.get("message", ""))

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.sqlservice.SqlService.insert_challenge_submission')
    def test_submission_failed_to_add_submission(self, mock_insert_submission, mock_get_challenge_tests_by_id, mock_get_challenge_by_id):
        mock_get_challenge_by_id.return_value = self.challenge
        mock_get_challenge_tests_by_id.return_value = [self.challenge_test]

        # Mock insert_challenge_submission to return False, simulating a failure to add submission
        mock_insert_submission.return_value = False

        with self.client.session_transaction() as session:
            session['user_id'] = 'test_user_id'  # Set user ID in session

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("message", ""), "Failed to add your submission.")
        self.assertEqual(response.json.get("flash", {}).get("message", ""), "Failed to add submission.")
        self.assertEqual(response.json.get("flash", {}).get("category", ""), "error")

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.dockerservice.DockerService.execute_code')
    def test_submission_execution_error(self, mock_execute_code, mock_get_tests, mock_get_challenge):
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]
        mock_execute_code.return_value = {'error': 'Execution Error', 'print_outputs': ['']}

        response = self.client.post('/submission/1', data={'stub-block': 'def foo(x, y): return x + y'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Execution Error', response.json.get('message'))
        self.assertIn('Execution Error', response.json.get('flash', {}).get('message'))
        self.assertEqual('error', response.json.get('flash', {}).get('category'))

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.dockerservice.DockerService.execute_code')
    def test_submission_exception_error(self, mock_execute_code, mock_get_tests, mock_get_challenge):
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]

        # Simulate the formatted exception message
        formatted_exception_message = "RuntimeError: Test Exception Occurred"
        mock_execute_code.return_value = {
            'exception': formatted_exception_message,
            'print_outputs': [''],
            'tests_passed': 0,
            'tests_total': 0
        }

        with self.client.session_transaction() as session:
            session['user_id'] = 'test_user_id'

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)
        print(response.data)

        self.assertEqual(response.status_code, 500)









if __name__ == '__main__':
    unittest.main()
