import sys
import os
import unittest
from unittest.mock import patch

# Add the parent directory to the PYTHONPATH so the App class can be imported
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import App
from classes.account.user import User

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        #Set up a test client before each test
        app = App().app
        app.testing = True
        self.client = app.test_client()

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

if __name__ == '__main__':
    unittest.main()
