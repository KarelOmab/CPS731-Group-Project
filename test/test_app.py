import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import App 
from flask import session



class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app_instance = App()
        self.test_client = self.app_instance.app.test_client()
        self.app_instance.app.testing = True
        # Other setup can go here

    def test_generic_challenge_success(self):
        # Assume you have a challenge in your database with an id of 1
        response = self.test_client.get('/challenges/1')  # Use the test client to make a request

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTrue(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertIn('Sum', response.data.decode('utf-8'))  # Check for challenge title
       

    def test_generic_challenge_failure(self):
        # Assume you have a challenge in your database with an id of 1
        response = self.test_client.get('/challenges/100')  # Use the test client to make a request

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check if the correct template was used
        self.assertFalse(b'/challenge' in response.data)

        # Check if the returned template title is correct
        self.assertNotIn('Sum', response.data.decode('utf-8'))  # Check for challenge title
       
    def test_index_success(self):
        # response from running  the index page
        response = self.test_client.get('/')  # Use the test client to make a request
       
        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTrue(b'/login' in response.data)

        # Check if the returned template title is correct
        self.assertIn("Welcome to Coding Challenge Web Application", response.data.decode('utf-8'))  # Check for challenge title
    #what would be the failure case for index page ????
    
    def test_challenges_success(self):
        with self.test_client as client:
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

    #def test_challenges_failure(self):

    def test_submit_challenge_success(self):
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges
                sess['priviledge'] = True  
                sess['userid'] = 1
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
            response = client.post('/submit_challenge', data=form_data)
            

            # Check the status code
            self.assertEqual(response.status_code, 302)

            # Check if the correct template was used
            self.assertTrue(b'challenges' in response.data, "The word 'challenges' was not found in the response")

            
            # Check if the newly added challenge is in the returned page
            self.assertTrue(b'Subtract' in response.data, "The word 'challenges' was not found in the response")

    
    def test_submit_challenge_failure(self):
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges
                sess['priviledge'] = False  
                sess['userid'] = 1
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
            response = client.post('/submit_challenge', data=form_data)
          

            # Check the status code
            self.assertEqual(response.status_code, 302)

            # Check if the correct template was used
            self.assertTrue(b'challenges' in response.data, "The word 'challenges' was not found in the response")

         # Check if the newly added challenge is in the returned page
            self.assertFalse(b'Add' in response.data, "The word 'challenges' was not found in the response")


    def test_submit_comment_success(self):
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['userid'] = 1
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
            self.assertTrue(b'Sum' in response.data, "The word 'challenges' was not found in the response")

         # Check if the newly added comment title exists in the return page
            #self.assertTrue(b'Very Easy' in response.data, "The word 'challenges' was not found in the response")

    #We have to make sure that the challenge with challenge_id 255 with name Are We Even exist in our database
    def test_delete_challenge_success(self):
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['userid'] = 1
                sess['priviledge'] = True  

            # Use the test client to simulate a POST request to your route
            response = client.get('/delete_challenge/255')
          
            # Check the status code
            self.assertEqual(response.status_code, 302)

            # Check if the deleted challenge exist in our returned page
            self.assertFalse(b'Are We Even?' in response.data, "The word 'challenges' was not found in the response")
    
    #We have to make sure that the challenge with challenge_id 2 with a name "Biggest Number" exist in our database
    def test_delete_challenge_failure(self):
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2

            # Use the test client to simulate a POST request to your route
            response = client.get('/delete_challenge/2')
          
            # Check the status code
            self.assertEqual(response.status_code, 302)

            # Check the challenge sum still in the page
            self.assertTrue(b'Biggest Number' in response.data, "The word 'challenges' was not found in the response")

    
    def test_edit_challenge_name_success(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_name': 'The Biggest Number'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_name/2', json = mock_json_data)

            # Check the status code
            self.assertEqual(response.status_code, 200)

            # Check the newly added name is in the return page
            self.assertTrue(b'The Biggest Number' in response.data, "The word 'challenges' was not found in the response")    

    def test_edit_challenge_name_failure(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_name': 'Biggest Number'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_name/2', json = mock_json_data)
          
          
            # Check the status code
            self.assertFalse(response.status_code, 200)

   
    
    def test_edit_challenge_difficulty_success(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'newValue': 'Hard'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_difficulty/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertEqual(response.status_code, 200)
    

    def test_edit_challenge_description_success(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_discr': 'No description available'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_description/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

            
            # Check the newly added discription is in the return page
            self.assertTrue(b'No description available' in response.data)    
        
    def test_edit_challenge_description_failure(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'new_challenge_discr': 'Finds the biggest number from the list'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_description/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertFalse(response.status_code, 200)

    def test_edit_challenge_stub_name_success(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'stub_name': 'max_number'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-name/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

            # Check the newly added stub-name exist in the return page
            self.assertTrue(b'max_number' in response.data)    
    
    def test_edit_challenge_stub_name_failure(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2

           

            #mocking the JSON data that is sent by the JavaScript
            mock_json_data = {'stub_name': 'max_integer'}

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-name/2', json = mock_json_data)
           
          
            # Check the status code
            self.assertFalse(response.status_code, 200)


    def test_edit_challenge_stub_block_success(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1

           

            #mocking the form data
            form_data = {
            'stub-block': 'def max_number\n  #Add your codes here'
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-block/2', data = form_data)
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

            # Check the newly added stub-block does exist in the return page
            self.assertTrue(b'#Add your codes here' in response.data)   

    def test_edit_challenge_stub_block_failure(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2

           

            #mocking the form data
            form_data = {
            'stub-block': 'def max_number\n  #your codes here'
            }

            # Use the test client to simulate a POST request to your route
            response = client.post('/edit_challenge_stub-block/2', data = form_data)
           
          
            # Check the status code
            self.assertFalse(response.status_code, 200)

    def test_add_test_case_success(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1

           

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
            self.assertTrue(b'[1,2,3,100,0]' in response.data) 
    
    def test_add_test_case_failure(self):
        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2

           

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
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1


            # Use the test client to simulate a POST request to your route
            response = client.post('/delete_test_case/2/6')
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)

            #test case with id = 6 has the input parameter = [0, -1, 1, -100, 100]
            # Check the delete test case input parameter doesn't exist in the returned page
            self.assertFalse(b'[0, -1, 1, -100, 100]' in response.data)   

    def test_delete_test_case_failure(self): 
         with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = False
                sess['userid'] = 2


            # Use the test client to simulate a POST request to your route
            # test case id = 4 has the following input parameter [1, 2, 3, 4, 5]
            response = client.post('/delete_test_case/2/4')
           
            # Check the attempted delete failed by looking for the input parameter of the test case in the returned data
            self.assertTrue(b'max_number ( [1, 2, 3, 4, 5] )' in response.data)   
          

    #Here we want to make sure that we have a comment for challenge id = 2 with comment id = 88 in the database
    def test_delete_comment_success(self):
        #, challenge_id, comment_id /delete_comment/

        with self.test_client as client:
            with client.session_transaction() as sess:
                # Set a session variable because I set the session variable in the index page so that there is a default sorting criteria for challenges  
                sess['priviledge'] = True
                sess['userid'] = 1


            # Use the test client to simulate a POST request to your route
            response = client.post('/delete_comment/2/88')
           
          
            # Check the status code
            self.assertTrue(response.status_code, 200)
       