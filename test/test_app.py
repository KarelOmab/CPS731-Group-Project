import sys
import os
import unittest
from unittest.mock import patch
from datetime import datetime
import re
from bs4 import BeautifulSoup

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
    def test_submission_execution_error(self, mock_execute_code, mock_get_tests, mock_get_challenge):
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]

        # Simulate an execution error scenario
        mock_execute_code.return_value = {
            'error': 'Execution Error',
            'print_outputs': [''],
            'tests_passed': 0,
            'tests_total': 1,
            'exec_time': 0,
            'exec_chars': 0
        }

        with self.client.session_transaction() as session:
            session['user_id'] = 'test_user_id'

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)

        self.assertEqual(response.status_code, 400)

    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.dockerservice.DockerService.execute_code')
    def test_submission_timeout(self, mock_execute_code, mock_get_tests, mock_get_challenge):
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]

        # Adjusted mock for a timeout scenario
        mock_execute_code.return_value = {
            'timeout': True,
            'print_outputs': [''],
            'tests_passed': 0,
            'tests_total': 1,
            'error': None,
            'exec_time': 0,
            'exec_chars': 0
        }

        with self.client.session_transaction() as session:
            session['user_id'] = 'test_user_id'

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)

        self.assertEqual(response.status_code, 408)
        self.assertIn("Timeout Occurred!", response.json.get('message'))
        self.assertIn("A timeout occurred during the execution of your submission.", response.json.get('flash', {}).get('message'))
        self.assertEqual('warning', response.json.get('flash', {}).get('category'))
    
    @patch('classes.util.sqlservice.SqlService.get_challenge_by_id')
    @patch('classes.util.sqlservice.SqlService.get_challenge_tests_by_id')
    @patch('classes.util.dockerservice.DockerService.execute_code')
    def test_submission_exception(self, mock_execute_code, mock_get_tests, mock_get_challenge):
        mock_get_challenge.return_value = self.challenge
        mock_get_tests.return_value = [self.challenge_test]

        # Simulate an exception scenario
        mock_execute_code.return_value = {
            'timeout': False,
            'exception': 'Exception occurred',
            'print_outputs': [''],
            'tests_passed': 0,
            'tests_total': 1,
            'error': None,
            'exec_time': 0,
            'exec_chars': 0
        }

        with self.client.session_transaction() as session:
            session['user_id'] = 'test_user_id'

        valid_test_data = {'stub-block': 'def foo(x, y): return x + y'}
        response = self.client.post('/submission/1', data=valid_test_data)

        self.assertEqual(response.status_code, 500)
        self.assertIn('Exception occurred', response.json.get('message'))
        self.assertIn('Exception occurred', response.json.get('flash', {}).get('message'))
        self.assertEqual('error', response.json.get('flash', {}).get('category'))

    def test_generic_challenge_success(self):
        response = self.client.get('/challenges/1')

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTrue(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertIn('Sum', response.data.decode('utf-8'))  # Check for challenge title

    def test_generic_challenge_failure(self):
        response = self.client.get('/challenges/100')

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check if the correct template was used
        self.assertFalse(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertNotIn('Sum', response.data.decode('utf-8'))  # Check for challenge title

    def test_challenges_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges
                sess['sorting_criteria'] = 'difficulty'  

            # Make the request to the /challenges route
            response = client.get('/challenges')

            # Check the status code
            self.assertEqual(response.status_code, 200)

            # Check if the correct template was used
            self.assertTrue(b'challenges' in response.data, "The word 'challenges' was not found in the response")

            # Check if the returned page contains the title 'Challenges'
            self.assertIn('Challenges', response.data.decode('utf-8'), "The title 'Challenges' was not found in the response")


    def test_submit_challenge_success(self):
         with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges
                sess['privileged_mode'] = True  
                sess['user_id'] = 1
                sess['sorting_criteria'] = 'name'
            #mock the form data for the new created challenge
            form_data = {
            'challengeName': 'Subtract',
            'challengeDifficulty': 'Easy',
            'challengeDescription': 'Given two numbers x and y, return x - y',
            'stubName': 'sub',
            'stubBlock': 'def sub(x,y)\n#Add your codes here',
            'timeAllowed': '20',
            'inputParameters[]': ['1,3','1,4','0,0'],
            'expectedOutput[]': ['-2','-3','0'],
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/submit_challenge', data = form_data , follow_redirects=True)

            
            # Check the status code
            self.assertEqual(response.status_code, 200)

            # Validate content type
            self.assertIn('text/html', response.content_type)

    def test_submit_challenge_failure(self):
         with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges
                sess['privileged_mode'] = False  
                sess['user_id'] = 1
                sess['sorting_criteria'] = 'name'

            #mock the form data for the new created challenge
            form_data = {
            'challengeName': 'Add',
            'challengeDifficulty': 'Easy',
            'challengeDescription': 'Given two numbers x and y, return x + y',
            'stubName': 'sub',
            'stubBlock': 'def add(x,y)\n#Add your codes here',
            'timeAllowed': '20',
            'inputParameters[]': ['1,3','1,4','0,0'],
            'expectedOutput[]': ['4','5','0'],
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/submit_challenge', data=form_data, follow_redirects=True)

            # Check the status code
            self.assertEqual(response.status_code, 200)

            # Check if the correct template was used
            self.assertTrue(b'challenges' in response.data, "The word 'challenges' was not found in the response")

         # Check if the newly added challenge is in the returned page
            self.assertFalse(b'Add' in response.data, "The word 'challenges' was not found in the response")

    def test_submit_comment_success(self):
         with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['user_id'] = 1
            #mock the form data for the new created challenge
            form_data = {
            'comment-title': 'Very Easy',
            'comment-content': 'Thank you for such an easy challenge',
            
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/submit_comment/1', data=form_data)
          
            # Check the status code
            self.assertEqual(response.status_code, 302)

            # Check if the correct template was used
            self.assertTrue(re.search(r'challenges', response.data.decode('utf-8')), "The word 'challenges' was not found in the response")            
           
    #We have to make sure that the challenge with challenge_id 255 with name Are We Even exist in our database
    def test_delete_challenge_success(self):
         with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['user_id'] = 1
                sess['privileged_mode'] = True  

            # Use the test client to simulate a POST request to your route
            response = client.get('/delete_challenge/255')
          
            # Check the status code
            self.assertEqual(response.status_code, 302)

            # Check if the deleted challenge exist in our returned page
            self.assertFalse(b'Are We Even?' in response.data, "The word 'challenges' was not found in the response")
    
    #We have to make sure that the challenge with challenge_id 2 with a name "Biggest Number" exist in our database
    def test_delete_challenge_failure(self):
         with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = False
                sess['user_id'] = 2

            # Use the test client to simulate a POST request to your route
            response = client.get('/delete_challenge/2')
          
            # Check the status code
            self.assertEqual(response.status_code, 302)

             # Validate content type
            self.assertIn('text/html', response.content_type)

            # Parse HTML response data
            soup = BeautifulSoup(response.data, 'html.parser')
        
            # Check for the presence of the challenges title
            pattern = re.compile(r'challenges') #Biggest\s+Number
            self.assertIsNotNone(soup.find(string=pattern), "The phrase 'challenges' was not found in the response")
    
    def test_edit_challenge_name_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_name': 'The Biggest Number'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_name/2', json = mock_json_data, follow_redirects=True)

            # Check the status code
            self.assertEqual(response.status_code, 200)

            #get the challenge/2 page for update
            response_2 = client.get("/challenges/2")
            #print(response_2.data.decode())

            # Validate content type
            self.assertIn('text/html', response_2.content_type)
            # <h2 class="card-title">The Biggest Number 

            soup = BeautifulSoup(response_2.data.decode(), 'html.parser')

            # Find the <p> tag with the specific text
            p_tag = soup.find('h2', class_='card-title')
            
            # Check if the text is exactly 'No description available'
            self.assertEqual(p_tag.get_text(strip=True), 'The Biggest NumberEdit')
           

    def test_edit_challenge_name_failure(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = False
                sess['user_id'] = 2

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_name': 'Biggest Number'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_name/2', json = mock_json_data)
          
          
            # Check the status code
            self.assertTrue(response.status_code, 302)

   
    
    def test_edit_challenge_difficulty_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'newValue': 'Hard'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_difficulty/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertEqual(response.status_code, 200)


            #get the challenge/2 page for update
            response_2 = client.get("/challenges/2")
            #print(response_2.data.decode())

            # Validate content type
            self.assertIn('text/html', response_2.content_type)
            #<h5 class="card-title">Difficulty: Hard  

            soup = BeautifulSoup(response_2.data.decode(), 'html.parser')

            # Find the <p> tag with the specific text
            p_tag = soup.find('h5', class_='card-title')
            
            # Check if the text is exactly 'No description available'
            self.assertEqual(p_tag.get_text(strip=True), 'Difficulty: HardEdit')

           

    def test_edit_challenge_description_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_discr': 'No description available'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_description/2', json = mock_json_data)

            # Check the status code
            self.assertTrue(response.status_code, 200)


            #get the challenge/2 page for update
            response_2 = client.get("/challenges/2")
            #print(response_2.data.decode())

            # Validate content type
            self.assertIn('text/html', response_2.content_type)

            soup = BeautifulSoup(response_2.data.decode(), 'html.parser')

            # Find the <p> tag with the specific text
            p_tag = soup.find('p', class_='card-text')
            
            # Check if the text is exactly 'No description available'
            self.assertEqual(p_tag.get_text(strip=True), 'Description: No description availableEdit')
            
          
           

        
    def test_edit_challenge_description_failure(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = False
                sess['user_id'] = 2

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_discr': 'Finds the biggest number from the list'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_description/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 302)

    def test_edit_challenge_stub_name_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'stub_name': 'max_number'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-name/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)
    
    def test_edit_challenge_stub_name_failure(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = False
                sess['user_id'] = 2

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'stub_name': 'max_integer'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-name/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)


    def test_edit_challenge_stub_block_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1

           

            #mocking the form data
            form_data = {
            'stub-block': 'def max_number\n  #Add your codes here'
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-block/2', data = form_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

           

    def test_edit_challenge_stub_block_failure(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = False
                sess['user_id'] = 2

           

            #mocking the form data
            form_data = {
            'stub-block': 'def max_number\n  #your codes here'
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-block/2', data = form_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

    def test_add_test_case_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1

           

            #mocking the form data
            form_data = {
            'inputParameters[]': '[1,2,3,100,0]',
            'expectedOutput[]': '100'
            }


            # Use the test client to simulate a POST request to your route
            response = client.post('add_test_case/2', data= form_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

            # Check the newly added test-case exist in the return page
            self.assertTrue(re.search(r'[1,2,3,100,0]',response.data.decode('utf-8')))
    
    def test_add_test_case_failure(self):
        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = False
                sess['user_id'] = 2

           

            #mocking the form data
            form_data = {
            'inputParameters[]': '[1,2,3,-2-3-1]',
            'expectedOutput[]': '3'
            }


            # Use the test client to simulate a POST request to your route
            response = client.post('add_test_case/2', data= form_data)

            # Check the newly added test-case exist in the return page
            self.assertFalse(b'[1,2,3,-2-3-1]' in response.data) 

    def test_delete_test_case_success(self): 
         with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1


            # Use the test client to simulate a POST request to your route
            response = client.post('/delete_test_case/2/6')
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

            #test case with id = 6 has the input parameter = [0, -1, 1, -100, 100]
            # Check the delete test case input parameter doesn't exist in the returned page
            self.assertFalse(b'[0, -1, 1, -100, 100]' in response.data)   
          

    #Here we want to make sure that we have a comment for challenge id = 2 with comment id = 88 in the database
    def test_delete_comment_success(self):
        #, challenge_id, comment_id /delete_comment/

        with self.client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['privileged_mode'] = True
                sess['user_id'] = 1


            # Use the test client to simulate a POST request to your route
            response = client.post('/delete_comment/2/88')
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)







if __name__ == '__main__':
    unittest.main()
