import unittest
from classes.util.sqlservice import SqlService

class TestMyClass(unittest.TestCase):
    
    def test_insert_account_success(self):
        # Define test data
        usergroup = 3
        username = "testuser" + "ae5deb822e0d71992900471a7199d0d95b8e7c9d05c40a8245a281fd2c1d6684"  #hash to guarantee uniqueness
        password = "testpassword123"
        email = "testuser@example.com"

        # Call the method
        result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

        # Assert that the result is as expected
        self.assertEqual(result, "Success")

        # Note receiving the message "Success" implies that the record was inserted
        # Additional cleanup code to remove the inserted data from the database
        SqlService.purge_account_by_username(username)  # purge this record

    def test_insert_account_fail_username_in_use(self):
            # Define test data
            usergroup = 2
            username = "karel"  #hash to guarantee uniqueness
            password = "testpassword123"
            email = "testuser@example.com"

            # Call the method
            result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

            # Assert that the result is as expected
            self.assertEqual(result, "Username in use")

    def test_insert_account_fail_email_in_use(self):
            # Define test data
            usergroup = 2
            username = "karel112"  #hash to guarantee uniqueness
            password = "testpassword123"
            email = "karel@email.com"

            # Call the method
            result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

            # Assert that the result is as expected
            self.assertEqual(result, "Email in use")

    def test_insert_challenge_success(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "Easy"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)[0]['LAST_INSERT_ID()']

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNotNone(challenge_id)
        
        # Optionally: Verify the inserted data in the database
        challenge = SqlService.get_challenge_by_id(challenge_id)
        SqlService.purge_challenge_by_id(challenge_id)  # purge this record
        self.assertEqual(challenge.name, name)
        self.assertEqual(challenge.difficulty, difficulty)
        self.assertEqual(challenge.description, description)
        self.assertEqual(challenge.stub_name, stub_name)
        self.assertEqual(challenge.stub_block, stub_block)
        self.assertEqual(challenge.time_allowed_sec, time_allowed_sec)

        

    def test_insert_challenge_fail_missing_account_id(self):
        # Define test data
        account_id = None # karel
        name = None
        difficulty = "Easy"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_name(self):
        # Define test data
        account_id = 1 # karel
        name = None
        difficulty = "Easy"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_difficulty(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = None
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_invalid_difficulty(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_description(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = None
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_stub_name(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = None
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_stub_block(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = None
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_time_allowed_sec(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = None

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_test_success(self):
        # Define test data
        challenge_id = 1
        input_data = "9, 10"
        output_data = "19"

        # Call the method
        challenge_test_id = SqlService.insert_challenge_test(challenge_id, input_data, output_data)[0]['LAST_INSERT_ID()']

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNotNone(challenge_test_id)

        # Optionally: Verify the inserted data in the database
        challenge_test = SqlService.get_challenge_test_by_id(challenge_test_id)
        SqlService.purge_challenge_test_by_id(challenge_test_id)  # purge this record
        self.assertEqual(challenge_test.test_input, input_data)
        self.assertEqual(challenge_test.test_output, output_data)

    def test_insert_challenge_test_fail_missing_input(self):
        # Define test data
        challenge_id = 1
        input_data = None
        output_data = "19"

        # Call the method
        challenge_test_id = SqlService.insert_challenge_test(challenge_id, input_data, output_data)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(challenge_test_id)

    def test_insert_challenge_test_fail_missing_output(self):
        # Define test data
        challenge_id = 1
        input_data = "9, 10"
        output_data = None

        # Call the method
        challenge_test_id = SqlService.insert_challenge_test(challenge_id, input_data, output_data)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(challenge_test_id)

    
    def test_insert_challenge_comment_success(self):
        # Define test data
        account_id = 1
        challenge_id = 1
        title = "Test Comment Title"
        text = "This is a test comment."

        # Call the method
        comment_id = SqlService.insert_challenge_comment(account_id, challenge_id, title, text)[0]['LAST_INSERT_ID()']

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNotNone(comment_id)

        # Optionally: Verify the inserted data in the database
        challenge_comment = SqlService.get_challenge_comment_by_id(comment_id)
        SqlService.purge_challenge_comment_by_id(comment_id)  # purge this record
        self.assertEqual(challenge_comment.title, title)
        self.assertEqual(challenge_comment.text, text)

    def test_insert_challenge_comment_fail_missing_account_id(self):
        # Define test data
        account_id = None
        challenge_id = 1
        title = "Test Comment Title"
        text = "This is a test comment."

        # Call the method
        comment_id = SqlService.insert_challenge_comment(account_id, challenge_id, title, text)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(comment_id)

    def test_insert_challenge_comment_fail_missing_challenge_id(self):
        # Define test data
        account_id = 1
        challenge_id = None
        title = "Test Comment Title"
        text = "This is a test comment."

        # Call the method
        comment_id = SqlService.insert_challenge_comment(account_id, challenge_id, title, text)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(comment_id)

    def test_insert_challenge_comment_fail_missing_title(self):
        # Define test data
        account_id = 1
        challenge_id = 1
        title = None
        text = "This is a test comment."

        # Call the method
        comment_id = SqlService.insert_challenge_comment(account_id, challenge_id, title, text)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(comment_id)

    def test_insert_challenge_comment_fail_missing_text(self):
        # Define test data
        account_id = 1
        challenge_id = 1
        title = "Test Comment Title"
        text = None

        # Call the method
        comment_id = SqlService.insert_challenge_comment(account_id, challenge_id, title, text)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(comment_id)

    def test_insert_challenge_submission_success(self):
        # Define test data
        challenge_id = 1
        account_id = 1
        exec_time = 1.23  # Execution time
        exec_chars = 100  # Number of characters
        exec_src = "return a+b"  # Example source code

        # Call the method
        submission_id = SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)[0]['LAST_INSERT_ID()']

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNotNone(submission_id)

        # Optionally: Verify the inserted data in the database
        challenge_submission = SqlService.get_challenge_submission_by_id(submission_id)
        SqlService.purge_challenge_submission_by_id(submission_id)  # purge this record
        self.assertEqual(challenge_submission.challenge_id, challenge_id)
        self.assertEqual(challenge_submission.account_id, account_id)
        self.assertEqual(challenge_submission.exec_time, exec_time)
        self.assertEqual(challenge_submission.exec_chars, exec_chars)
        self.assertEqual(challenge_submission.exec_src, exec_src)

    def test_insert_challenge_submission_fail_missing_challenge_id(self):
        # Define test data
        challenge_id = None
        account_id = 1
        exec_time = 1.23  # Execution time
        exec_chars = 100  # Number of characters
        exec_src = "return a+b"  # Example source code

        # Call the method
        submission_id = SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(submission_id)

    def test_insert_challenge_submission_fail_missing_account_id(self):
        # Define test data
        challenge_id = 1
        account_id = None
        exec_time = 1.23  # Execution time
        exec_chars = 100  # Number of characters
        exec_src = "return a+b"  # Example source code

        # Call the method
        submission_id = SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(submission_id)

    def test_insert_challenge_submission_fail_missing_exec_time(self):
        # Define test data
        challenge_id = 1
        account_id = 1
        exec_time = None
        exec_chars = 100  # Number of characters
        exec_src = "return a+b"  # Example source code

        # Call the method
        submission_id = SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(submission_id)

    def test_insert_challenge_submission_fail_missing_chars(self):
        # Define test data
        challenge_id = 1
        account_id = 1
        exec_time = 1.23  # Execution time
        exec_chars = None
        exec_src = "return a+b"  # Example source code

        # Call the method
        submission_id = SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(submission_id)

    def test_insert_challenge_submission_fail_missing_src(self):
        # Define test data
        challenge_id = 1
        account_id = 1
        exec_time = 1.23  # Execution time
        exec_chars = 100  # Number of characters
        exec_src = None

        # Call the method
        submission_id = SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(submission_id)

    def test_get_account_by_username_password_success(self):
        # Define test data
        username = "test"  
        password = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"  

        # Call the method
        account = SqlService.get_account_by_username_password(username, password)

        # Assert that the account is retrieved correctly
        self.assertIsNotNone(account)
        self.assertEqual(account.username, username)

    def test_get_account_by_username_password_fail_missing_username(self):
        # Define test data
        username = None 
        password = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"  

        # Call the method
        account = SqlService.get_account_by_username_password(username, password)

        # Assert that the account is retrieved correctly
        self.assertIsNone(account)

    def test_get_account_by_username_password_fail_missing_password(self):
        # Define test data
        username = "test" 
        password = None

        # Call the method
        account = SqlService.get_account_by_username_password(username, password)

        # Assert that the account is retrieved correctly
        self.assertIsNone(account)

    def test_get_all_challenges_success(self):
        # Call the method
        challenges = SqlService.get_all_challenges()

        # Assert that a list is returned
        self.assertIsInstance(challenges, list)

    def test_get_challenge_by_id_success(self):
        # Define test data
        challenge_id = 1

        # Call the method
        challenge = SqlService.get_challenge_by_id(challenge_id)

        # Assert that a challenge object is returned
        self.assertIsNotNone(challenge)
        self.assertEqual(challenge.id, challenge_id)

    def test_get_challenge_by_id_fail_missing_challenge_id(self):
        # Define test data
        challenge_id = None

        # Call the method
        challenge = SqlService.get_challenge_by_id(challenge_id)

        # Assert that a challenge object is returned
        self.assertIsNone(challenge)

    def test_get_challenge_tests_by_id_success(self):
        # Define test data
        challenge_id = 1

        # Call the method
        tests = SqlService.get_challenge_tests_by_id(challenge_id)

        # Assert that a list of tests is returned
        self.assertIsInstance(tests, list)

    def test_get_challenge_tests_by_id_fail_missing_id(self):
        # Define test data
        challenge_id = None

        # Call the method
        tests = SqlService.get_challenge_tests_by_id(challenge_id)

        # Assert that a list of tests is returned
        self.assertIsNone(tests)

    def test_get_challenge_comments_by_id_success(self):
        # Define test data
        challenge_id = 1

        # Call the method
        comments = SqlService.get_challenge_comments_by_id(challenge_id)

        # Assert that a list of comments is returned
        self.assertIsInstance(comments, list)

    def test_get_challenge_comments_by_id_fail_missing_challenge_id(self):
        # Define test data
        challenge_id = None

        # Call the method
        comments = SqlService.get_challenge_comments_by_id(challenge_id)

        self.assertIsNone(comments)

    def test_get_challenge_submissions_by_id_and_account_id_success(self):
        # Define test data
        challenge_id = 1
        account_id = 1

        # Call the method
        submissions = SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)

        # Assert that a list of submissions is returned
        self.assertIsInstance(submissions, list)

    def test_get_challenge_submissions_by_id_and_account_id_fail_missing_challenge_id(self):
        # Define test data
        challenge_id = None
        account_id = 1

        # Call the method
        submissions = SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)

        self.assertIsNone(submissions)

    def test_get_challenge_submissions_by_id_and_account_id_fail_missing_account_id(self):
        # Define test data
        challenge_id = 1
        account_id = None

        # Call the method
        submissions = SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)

        self.assertIsNone(submissions)

    def test_update_challenge_name_by_id_success(self):
        # Define test data
        challenge_id = 1

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        new_name = "Updated Challenge Name"

        # Call the method to update the challenge name
        update_result = SqlService.update_challenge_name_by_id(challenge_id, new_name)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the name change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.name, new_name)

        # Optionally, reset the name to its original value
        update_result = SqlService.update_challenge_name_by_id(challenge_id, original_challenge.name)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_name_by_id_fail_missing_challenge_name(self):
        # Define test data
        challenge_id = 1
        new_name = None

        # Call the method to update the challenge name
        update_result = SqlService.update_challenge_name_by_id(challenge_id, new_name)

        # Assert that the update was successful
        self.assertIsNone(update_result)

    def test_update_challenge_difficulty_by_id_success_easy(self):
        # Define test data
        challenge_id = 1

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        new_difficulty = "Easy"  # Choose from 'Easy', 'Medium', 'Hard'

        # Call the method to update the challenge difficulty
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, new_difficulty)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the difficulty change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.difficulty, new_difficulty)

        # Optionally, reset the name to its original value
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, original_challenge.difficulty)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_difficulty_by_id_success_medium(self):
        # Define test data
        challenge_id = 1

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        new_difficulty = "Medium"  # Choose from 'Easy', 'Medium', 'Hard'

        # Call the method to update the challenge difficulty
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, new_difficulty)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the difficulty change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.difficulty, new_difficulty)

        # Optionally, reset the name to its original value
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, original_challenge.difficulty)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_difficulty_by_id_success_medium(self):
        # Define test data
        challenge_id = 1

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        new_difficulty = "Hard"  # Choose from 'Easy', 'Medium', 'Hard'

        # Call the method to update the challenge difficulty
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, new_difficulty)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the difficulty change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.difficulty, new_difficulty)

        # Optionally, reset the name to its original value
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, original_challenge.difficulty)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_difficulty_by_id_fail_invalid_difficulity(self):
        # Define test data
        challenge_id = 1

        new_difficulty = "FooBar"  # Choose from 'Easy', 'Medium', 'Hard'

        # Call the method to update the challenge difficulty
        update_result = SqlService.update_challenge_difficulty_by_id(challenge_id, new_difficulty)

        # Assert that the update was successful
        self.assertIsNone(update_result)

    def test_update_challenge_description_by_id_success(self):
        # Define test data
        challenge_id = 1  # Replace with an actual challenge ID

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        new_description = "Updated description for the challenge."

        # Call the method to update the challenge description
        update_result = SqlService.update_challenge_description_by_id(challenge_id, new_description)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the description change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.description, new_description)

        # Optionally, reset the description to its original value
        update_result = SqlService.update_challenge_description_by_id(challenge_id, original_challenge.description)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_description_by_id_fail_missing_description(self):
        # Define test data
        challenge_id = 1
        new_description = None

        # Call the method to update the challenge description
        update_result = SqlService.update_challenge_description_by_id(challenge_id, new_description)

        # Assert that the update was successful
        self.assertIsNone(update_result)

    def test_update_challenge_stub_name_by_id_success(self):
        # Define test data
        challenge_id = 1

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)
        new_stub_name = "UpdatedStubName"

        # Call the method to update the challenge stub name
        update_result = SqlService.update_challenge_stub_name_by_id(challenge_id, new_stub_name)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the stub name change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.stub_name, new_stub_name)

        # Optionally, reset the stub name to its original value
        update_result = SqlService.update_challenge_stub_name_by_id(challenge_id, original_challenge.stub_name)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_stub_name_by_id_fail_missing_stub_name(self):
        # Define test data
        challenge_id = 1
        new_stub_name = None

        # Call the method to update the challenge stub name
        update_result = SqlService.update_challenge_stub_name_by_id(challenge_id, new_stub_name)

        # Assert that the update was successful
        self.assertIsNone(update_result)

    def test_update_challenge_stub_block_by_id_success(self):
        # Define test data
        challenge_id = 1  # Replace with an actual challenge ID

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        new_stub_block = "Updated stub block content"

        # Call the method to update the challenge stub block
        update_result = SqlService.update_challenge_stub_block_by_id(challenge_id, new_stub_block)

        # Assert that the update was successful
        self.assertTrue(update_result)

        # Fetch the updated challenge to verify the stub block change
        updated_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(updated_challenge.stub_block, new_stub_block)

        # Optionally, reset the stub block to its original value
        update_result = SqlService.update_challenge_stub_block_by_id(challenge_id, original_challenge.stub_block)

        # Assert that the update was successful
        self.assertTrue(update_result)

    def test_update_challenge_stub_block_by_id_fail_missing_stub_block(self):
        # Define test data
        challenge_id = 1  # Replace with an actual challenge ID
        new_stub_block = None

        # Call the method to update the challenge stub block
        update_result = SqlService.update_challenge_stub_block_by_id(challenge_id, new_stub_block)

        # Assert that the update was successful
        self.assertIsNone(update_result)

    def test_delete_challenge_by_id_success(self):
        # note we dont actually delete challenges but simply flag their is_deleted to 1 or 0
        # Define test data
        challenge_id = 1
        IS_DELETED = 1

        # Fetch the original challenge
        original_challenge = SqlService.get_challenge_by_id(challenge_id)

        # Call the method to delete the challenge
        delete_result = SqlService.update_challenge_is_deleted_by_id(challenge_id, IS_DELETED)

        # Assert that the deletion was successful
        self.assertTrue(delete_result)

        # Fetch the challenge to verify it is marked as deleted
        deleted_challenge = SqlService.get_challenge_by_id(challenge_id)
        self.assertEqual(deleted_challenge.is_deleted, IS_DELETED)

        # Optionally, reset the is deleted to its original value
        delete_result = SqlService.update_challenge_is_deleted_by_id(challenge_id, original_challenge.is_deleted)

        # Assert that the deletion was successful
        self.assertTrue(delete_result)

    def test_delete_challenge_test_by_id_and_challenge_id_success(self):
        # note we dont actually delete challenge tests but simply flag their is_deleted to 1 or 0
        # Define test data
        challenge_test_id = 2
        IS_DELETED = 1

        # Fetch the original challenge test
        original_challenge_test = SqlService.get_challenge_test_by_id(challenge_test_id)

        # Call the method to delete the challenge test
        delete_result = SqlService.update_challenge_test_is_deleted_by_id(challenge_test_id, IS_DELETED)

        # Assert that the deletion was successful
        self.assertTrue(delete_result)

        # Fetch the challenge test to verify it is marked as deleted
        deleted_challenge_test = SqlService.get_challenge_test_by_id(challenge_test_id)
        self.assertEqual(deleted_challenge_test.is_deleted, IS_DELETED)

        # Optionally, reset the is deleted to its original value
        delete_result = SqlService.update_challenge_test_is_deleted_by_id(challenge_test_id, original_challenge_test.is_deleted)

        # Assert that the deletion was successful
        self.assertTrue(delete_result)

    def test_delete_challenge_comment_by_id_and_challenge_id_success(self):
        # note we dont actually delete challenge comments but simply flag their is_deleted to 1 or 0
        # Define test data
        comment_id = 1
        IS_DELETED = 1

        # Fetch the original challenge comment
        original_challenge_comment = SqlService.get_challenge_comment_by_id(comment_id)

        # Call the method to delete the challenge comment
        delete_result = SqlService.update_challenge_comment_is_deleted_by_id(comment_id, IS_DELETED)

        # Assert that the deletion was successful
        self.assertTrue(delete_result)

        # Fetch the challenge comment to verify it is marked as deleted
        deleted_challenge_comment = SqlService.get_challenge_comment_by_id(comment_id)
        self.assertEqual(deleted_challenge_comment.is_deleted, IS_DELETED)

        # Optionally, reset the is deleted to its original value
        delete_result = SqlService.update_challenge_comment_is_deleted_by_id(comment_id, original_challenge_comment.is_deleted)

        # Assert that the deletion was successful
        self.assertTrue(delete_result)
  
if __name__ == '__main__':
    unittest.main()