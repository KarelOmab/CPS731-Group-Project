import unittest
from unittest.mock import patch, MagicMock
from classes.util.sqlservice import SqlService
from unittest.mock import patch
from classes.account.user import User
from classes.account.moderator import Moderator
from classes.challenge.challenge import Challenge
from classes.challenge.challengetest import ChallengeTest
from classes.challenge.challengecomment import ChallengeComment
from classes.challenge.challengesubmission import ChallengeSubmission
from datetime import datetime
import mysql.connector


# The purpose of these mock tests is to do line coverage
# These testers simply test line execution
# We have a separate integration test file for actual (real data) pushing/pulling

class TestSqlService(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_create_connection(self, mock_connect):
        SqlService.create_connection()
        mock_connect.assert_called_with(host=SqlService.HOST, user=SqlService.USER, password=SqlService.PASSWORD, database=SqlService.DATABASE)

    @patch('mysql.connector.connect')
    def test_execute_query(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Foo'}]

        result = SqlService.execute_query("SELECT * FROM challenges")

        self.assertEqual(result, [{'id': 1, 'name': 'Foo'}])
        mock_cursor.execute.assert_called_once_with("SELECT * FROM challenges", None)
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('classes.util.sqlservice.SqlService.create_connection')
    def test_execute_query_exception(self, mock_create_connection):
        # Setup a mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simulate an exception when cursor.execute is called
        mock_cursor.execute.side_effect = mysql.connector.Error("Test error")

        # Call the execute_query method
        result = SqlService.execute_query("SELECT * FROM challenges")

        # Assert that the result is None due to the exception
        self.assertIsNone(result)

        # Assert that the exception handling code was executed
        mock_cursor.execute.assert_called_once_with("SELECT * FROM challenges", None)
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('mysql.connector.connect')
    def test_execute_query_and_get_last_id(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.lastrowid = 1

        result = SqlService.execute_query_and_get_last_id("INSERT INTO usergroup (type) VALUES (%s)", ("guest",))

        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with("INSERT INTO usergroup (type) VALUES (%s)", ("guest",))
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('classes.util.sqlservice.SqlService.create_connection')
    def test_execute_query_and_get_last_id_exception(self, mock_create_connection):
        # Setup a mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simulate an exception when cursor.execute is called
        mock_cursor.execute.side_effect = mysql.connector.Error("Test error")

        # Call the execute_query_and_get_last_id method
        result = SqlService.execute_query_and_get_last_id("INSERT INTO usergroup (type) VALUES (%s)", ("guest",))

        # Assert that the result is None due to the exception
        self.assertIsNone(result)

        # Assert that the exception handling code was executed
        mock_cursor.execute.assert_called_once_with("INSERT INTO usergroup (type) VALUES (%s)", ("guest",))
        mock_connection.rollback.assert_called()
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('mysql.connector.connect')
    def test_call_stored_procedure(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [{'id': 1, 'name': 'Foo'}]
        mock_cursor.stored_results.return_value = [mock_result]

        result = SqlService.call_stored_procedure("GetChallengeById", params=(1,))

        self.assertEqual(result, [{'id': 1, 'name': 'Foo'}])
        mock_cursor.callproc.assert_called_once_with("GetChallengeById", (1,))
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('classes.util.sqlservice.SqlService.create_connection')
    def test_call_stored_procedure_fetchone(self, mock_create_connection):
        # Setup mock connection, cursor, and stored result
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_stored_result = MagicMock()
        mock_stored_result.fetchone.return_value = {'id': 1, 'name': 'Foo'}
        mock_cursor.stored_results.return_value = [mock_stored_result]
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Call the method
        result = SqlService.call_stored_procedure("GetChallengeById", params=(1,), fetchone=True)

        # Assertions
        self.assertEqual(result, {'id': 1, 'name': 'Foo'})
        mock_cursor.callproc.assert_called_with("GetChallengeById", (1,))
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('classes.util.sqlservice.SqlService.create_connection')
    def test_call_stored_procedure_exception(self, mock_create_connection):
        # Setup mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simulate an exception when cursor.callproc is called
        mock_cursor.callproc.side_effect = mysql.connector.Error("Test error")

        # Call the method
        result = SqlService.call_stored_procedure("GetChallengeById", params=(1,))

        # Assertions
        self.assertIsNone(result)
        mock_cursor.callproc.assert_called_with("GetChallengeById", (1,))
        mock_connection.rollback.assert_called()
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()

    @patch('classes.util.sqlservice.SqlService.create_connection')
    def test_call_stored_procedure_update_or_delete(self, mock_create_connection):
        # Setup a mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Call the method with update=True
        result_update = SqlService.call_stored_procedure("UpdateChallengeNameById", params=(1, "Bar"), update=True)

        # Assertions for update
        self.assertTrue(result_update)
        mock_cursor.callproc.assert_called_with("UpdateChallengeNameById", (1, "Bar"))

        # Resetting mock for the next call
        mock_cursor.reset_mock()

        # Call the method with delete=True
        result_delete = SqlService.call_stored_procedure("DeleteChallengeById", params=(1,), delete=True)

        # Assertions for delete
        self.assertTrue(result_delete)
        mock_cursor.callproc.assert_called_with("DeleteChallengeById", (1, ))

        # Verify cursor and connection are closed
        self.assertEqual(mock_cursor.close.call_count, 1)
        self.assertEqual(mock_connection.close.call_count, 2)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_insert_account(self, mock_call_proc):
        usergroup, username, password, email = 'user', 'testuser', 'password', 'test@example.com'
        SqlService.insert_account(usergroup, username, password, email)
        mock_call_proc.assert_called_with("InsertAccount", params=(usergroup, username, password, email))

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_insert_challenge(self, mock_call_proc):
        account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec = 1, 'Foo', 'Easy', 'Description', 'foo', '# TODO', 10
        SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)
        mock_call_proc.assert_called_with("InsertChallenge", params=(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec))

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_insert_challenge_test(self, mock_call_proc):
        challenge_id, input_data, output_data = 1, 'input', 'output'
        SqlService.insert_challenge_test(challenge_id, input_data, output_data)
        mock_call_proc.assert_called_with("InsertChallengeTest", params=(challenge_id, input_data, output_data))

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_insert_challenge_comment(self, mock_call_proc):
        account_id, challenge_id, title, text = 1, 2, 'Comment Title', 'Comment Text'
        
        # Set up a mock return value for call_stored_procedure (assuming it returns the new comment's ID)
        mock_call_proc.return_value = 123  # Example comment ID

        result = SqlService.insert_challenge_comment(account_id, challenge_id, title, text)

        # Verify that call_stored_procedure was called correctly
        mock_call_proc.assert_called_with("InsertChallengeComment", params=(account_id, challenge_id, title, text))

        # Verify that the result matches the expected return value
        self.assertEqual(result, 123)


    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_insert_challenge_submission(self, mock_call_proc):
        challenge_id, account_id, exec_time, exec_chars, exec_src = 1, 1, 5.0, 100, 'source code'
        SqlService.insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src)
        mock_call_proc.assert_called_with("InsertChallengeSubmission", params=(challenge_id, account_id, exec_time, exec_chars, exec_src))

    def test_raw_account_to_account(self):
        raw_account = {
            'id': 1,
            'created_at': datetime.now(),
            'usergroup_id': 2,
            'username': 'moduser',
            'email': 'mod@example.com'
        }
        account = SqlService.raw_account_to_account(raw_account)
        self.assertIsInstance(account, Moderator)
        self.assertEqual(account.username, 'moduser')

        raw_account['usergroup_id'] = 3  # Assuming 3 represents User
        account = SqlService.raw_account_to_account(raw_account)
        self.assertIsInstance(account, User)
        self.assertEqual(account.username, 'moduser')

        self.assertIsNone(SqlService.raw_account_to_account(None))

    def test_raw_account_to_account_none(self):
        # Test with raw_account as None
        result_none = SqlService.raw_account_to_account(None)
        self.assertIsNone(result_none)

        # Test with unrecognized usergroup_id
        raw_account_unrecognized = {
            'id': 123,
            'created_at': '2021-01-01T00:00:00Z',
            'usergroup_id': 999,  # Unrecognized usergroup_id
            'username': 'unknownUser',
            'email': 'unknown@example.com'
        }
        result_unrecognized = SqlService.raw_account_to_account(raw_account_unrecognized)
        self.assertIsNone(result_unrecognized)

    

    def test_raw_challenge_to_challenge(self):
        raw_challenge = {
            'id': 1,
            'created_at': datetime.now(),
            'account_id': 1,
            'is_deleted': False,
            'name': 'Foo',
            'difficulty': 'Easy',
            'description': 'Description',
            'stub_name': 'foo',
            'stub_block': '# TODO',
            'time_allowed_sec': 30
        }
        challenge = SqlService.raw_challenge_to_challenge(raw_challenge)
        self.assertIsInstance(challenge, Challenge)
        self.assertEqual(challenge.name, 'Foo')
        self.assertIsNone(SqlService.raw_challenge_to_challenge(None))
    
    def test_raw_challenge_to_challenge(self):
        raw_challenge = {
            'id': 1,
            'created_at': datetime.now(),
            'account_id': 1,
            'is_deleted': False,
            'name': 'Foo',
            'difficulty': 'Easy',
            'description': 'Description',
            'stub_name': 'foo',
            'stub_block': '# TODO',
            'time_allowed_sec': 30
        }
        challenge = SqlService.raw_challenge_to_challenge(raw_challenge)
        self.assertIsInstance(challenge, Challenge)
        self.assertEqual(challenge.name, 'Foo')
        self.assertIsNone(SqlService.raw_challenge_to_challenge(None))

    def test_raw_test_to_test(self):
        raw_test = {
            'id': 1,
            'challenge_id': 1,
            'is_deleted': False,
            'input': 'input data',
            'output': 'output data'
        }
        test = SqlService.raw_test_to_test(raw_test)
        self.assertIsInstance(test, ChallengeTest)
        self.assertEqual(test.test_input, 'input data')

    def test_raw_comment_to_comment(self):
        raw_comment = {
            'id': 1,
            'created_at': datetime.now(),
            'account_id': 1,
            'is_deleted': False,
            'challenge_id': 1,
            'title': 'Title',
            'text': 'Text',
            'username': 'user'
        }
        comment = SqlService.raw_comment_to_comment(raw_comment)
        self.assertIsInstance(comment, ChallengeComment)
        self.assertEqual(comment.title, 'Title')

    def test_raw_submission_to_submission(self):
        raw_submission = {
            'id': 1,
            'created_at': datetime.now(),
            'challenge_id': 1,
            'account_id': 1,
            'exec_time': 5.0,
            'exec_chars': 100,
            'exec_src': 'source code'
        }
        submission = SqlService.raw_submission_to_submission(raw_submission)
        self.assertIsInstance(submission, ChallengeSubmission)
        self.assertEqual(submission.exec_time, 5.0)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_account_to_account')
    def test_get_account_by_username_password(self, mock_transform, mock_call_proc):
        username, password = 'testuser', 'password'
        SqlService.get_account_by_username_password(username, password)
        mock_call_proc.assert_called_with("GetAccountByUsernameAndPassword", params=(username, password), fetchone=True)
        mock_transform.assert_called()

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_challenge_to_challenge')
    def test_get_all_challenges(self, mock_transform, mock_call_proc):
        # Mock return value for call_stored_procedure
        mock_call_proc.return_value = [
            {'id': 1, 'name': 'Challenge 1'}, 
            {'id': 2, 'name': 'Challenge 2'}
        ]

        SqlService.get_all_challenges()

        # Verify that call_stored_procedure was called correctly
        mock_call_proc.assert_called_with("GetAllChallenges")

        # Verify that raw_challenge_to_challenge was called for each raw challenge
        self.assertEqual(mock_transform.call_count, 2)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_challenge_to_challenge')
    def test_get_challenge_by_id(self, mock_transform, mock_call_proc):
        challenge_id = 1
        SqlService.get_challenge_by_id(challenge_id)
        mock_call_proc.assert_called_with("GetChallengeById", params=(challenge_id, ), fetchone=True)
        mock_transform.assert_called()

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_test_to_test')
    def test_get_challenge_test_by_id(self, mock_transform, mock_call_proc):
        challenge_test_id = 1
        SqlService.get_challenge_test_by_id(challenge_test_id)
        mock_call_proc.assert_called_with("GetChallengeTestById", params=(challenge_test_id, ), fetchone=True)
        mock_transform.assert_called()

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_test_to_test')
    def test_get_challenge_tests_by_id(self, mock_transform, mock_call_proc):
        # Mock return value for call_stored_procedure
        challenge_id = 1
        mock_call_proc.return_value = [
            {'id': 1, 'input': 'test input 1', 'output': 'test output 1'}, 
            {'id': 2, 'input': 'test input 2', 'output': 'test output 2'}
        ]

        SqlService.get_challenge_tests_by_id(challenge_id)

        # Verify that call_stored_procedure was called correctly
        mock_call_proc.assert_called_with("GetChallengeTestsById", params=(challenge_id,))

        # Verify that raw_test_to_test was called for each raw test
        self.assertEqual(mock_transform.call_count, 2)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_get_challenge_tests_by_id_none(self, mock_call_proc):
        # Challenge ID to test
        challenge_id = 1

        # Mock call_stored_procedure to return None or an empty list
        mock_call_proc.return_value = None

        # Call the method
        result = SqlService.get_challenge_tests_by_id(challenge_id)

        # Assertions
        self.assertIsNone(result)
        mock_call_proc.assert_called_with("GetChallengeTestsById", params=(challenge_id, ))

        # Reset and test with an empty list
        mock_call_proc.reset_mock()
        mock_call_proc.return_value = []

        # Call the method again
        result = SqlService.get_challenge_tests_by_id(challenge_id)

        # Assertions
        self.assertIsNone(result)
        mock_call_proc.assert_called_with("GetChallengeTestsById", params=(challenge_id, ))

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_test_to_test')
    def test_get_challenge_tests_by_id_and_limit(self, mock_transform, mock_call_proc):
        # Set challenge ID and expected limit
        challenge_id = 1
        expected_limit = 5

        # Mock return value for call_stored_procedure
        mock_call_proc.return_value = [
            {'id': 1, 'input': 'test input 1', 'output': 'test output 1'},
            {'id': 2, 'input': 'test input 2', 'output': 'test output 2'}
        ]

        tests = SqlService.get_challenge_tests_by_id_and_limit(challenge_id)

        # Verify that call_stored_procedure was called with the correct parameters
        mock_call_proc.assert_called_with("GetChallengeTestsByIdAndLimit", params=(challenge_id, expected_limit))

        # Verify that raw_test_to_test was called for each raw test
        self.assertEqual(mock_transform.call_count, 2)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_comment_to_comment')
    def test_get_challenge_comment_by_id(self, mock_transform, mock_call_proc):
        comment_id = 1
        SqlService.get_challenge_comment_by_id(comment_id)
        mock_call_proc.assert_called_with("GetChallengeCommentById", params=(comment_id, ), fetchone=True)
        mock_transform.assert_called()

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_comment_to_comment')
    def test_get_challenge_comments_by_id(self, mock_transform, mock_call_proc):
        # Mock return value for call_stored_procedure
        challenge_id = 1
        mock_call_proc.return_value = [
            {'id': 1, 'title': 'Comment 1', 'text': 'Text 1'}, 
            {'id': 2, 'title': 'Comment 2', 'text': 'Text 2'}
        ]

        SqlService.get_challenge_comments_by_id(challenge_id)

        # Verify that call_stored_procedure was called correctly
        mock_call_proc.assert_called_with("GetChallengeCommentsById", params=(challenge_id, ))

        # Verify that raw_comment_to_comment was called for each raw comment
        self.assertEqual(mock_transform.call_count, 2)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_get_challenge_comments_by_id_none(self, mock_call_proc):
        # Challenge ID to test
        challenge_id = 1

        # Mock call_stored_procedure to return None
        mock_call_proc.return_value = None

        # Call the method
        result = SqlService.get_challenge_comments_by_id(challenge_id)

        # Assertions
        self.assertIsNone(result)
        mock_call_proc.assert_called_with("GetChallengeCommentsById", params=(challenge_id, ))

        # Reset and test with an empty list
        mock_call_proc.reset_mock()
        mock_call_proc.return_value = []

        # Call the method again
        result = SqlService.get_challenge_comments_by_id(challenge_id)

        # Assertions
        self.assertIsNone(result)
        mock_call_proc.assert_called_with("GetChallengeCommentsById", params=(challenge_id, ))

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_submission_to_submission')
    def test_get_challenge_submission_by_id(self, mock_transform, mock_call_proc):
        submission_id = 1
        SqlService.get_challenge_submission_by_id(submission_id)
        mock_call_proc.assert_called_with("GetChallengeSubmissionById", params=(submission_id, ), fetchone=True)
        mock_transform.assert_called()

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    @patch('classes.util.sqlservice.SqlService.raw_submission_to_submission')
    def test_get_challenge_submissions_by_id_and_account_id(self, mock_transform, mock_call_proc):
        # Mock return value for call_stored_procedure
        challenge_id, account_id = 1, 1
        mock_call_proc.return_value = [
            {'id': 1, 'exec_time': 1.2, 'exec_chars': 100, 'exec_src': 'source code 1'}, 
            {'id': 2, 'exec_time': 1.5, 'exec_chars': 200, 'exec_src': 'source code 2'}
        ]

        SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)

        # Verify that call_stored_procedure was called correctly
        mock_call_proc.assert_called_with("GetChallengeSubmissionsByIdAndAccountId", params=(challenge_id, account_id))

        # Verify that raw_submission_to_submission was called for each raw submission
        self.assertEqual(mock_transform.call_count, 2)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_get_challenge_submissions_by_id_and_account_id_none(self, mock_call_proc):
        # Set challenge_id and account_id
        challenge_id, account_id = 1, 1

        # Mock call_stored_procedure to return None
        mock_call_proc.return_value = None

        # Call the method
        result = SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)

        # Assertions
        self.assertIsNone(result)
        mock_call_proc.assert_called_with("GetChallengeSubmissionsByIdAndAccountId", params=(challenge_id, account_id))

        # Reset and test with an empty list
        mock_call_proc.reset_mock()
        mock_call_proc.return_value = []

        # Call the method again
        result = SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)

        # Assertions
        self.assertIsNone(result)
        mock_call_proc.assert_called_with("GetChallengeSubmissionsByIdAndAccountId", params=(challenge_id, account_id))

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_name_by_id(self, mock_call_proc):
        challenge_id, name = 1, 'New Challenge Name'
        result = SqlService.update_challenge_name_by_id(challenge_id, name)
        mock_call_proc.assert_called_with("UpdateChallengeNameById", params=(challenge_id, name), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_difficulty_by_id(self, mock_call_proc):
        challenge_id, difficulty = 1, 'Medium'
        result = SqlService.update_challenge_difficulty_by_id(challenge_id, difficulty)
        mock_call_proc.assert_called_with("UpdateChallengeDifficultyById", params=(challenge_id, difficulty), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_description_by_id(self, mock_call_proc):
        challenge_id, description = 1, 'New Description'
        result = SqlService.update_challenge_description_by_id(challenge_id, description)
        mock_call_proc.assert_called_with("UpdateChallengeDescriptionById", params=(challenge_id, description), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_stub_name_by_id(self, mock_call_proc):
        challenge_id, name = 1, 'New Stub Name'
        result = SqlService.update_challenge_stub_name_by_id(challenge_id, name)
        mock_call_proc.assert_called_with("UpdateChallengeStubNameById", params=(challenge_id, name), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_stub_block_by_id(self, mock_call_proc):
        challenge_id, stub_block = 1, 'New Stub Block'
        result = SqlService.update_challenge_stub_block_by_id(challenge_id, stub_block)
        mock_call_proc.assert_called_with("UpdateChallengeStubBlockById", params=(challenge_id, stub_block), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_is_deleted_by_id(self, mock_call_proc):
        challenge_id, is_deleted = 1, True
        result = SqlService.update_challenge_is_deleted_by_id(challenge_id, is_deleted)
        mock_call_proc.assert_called_with("UpdateChallengeIsDeletedById", params=(challenge_id, is_deleted), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_test_is_deleted_by_id(self, mock_call_proc):
        challenge_test_id, is_deleted = 1, True
        result = SqlService.update_challenge_test_is_deleted_by_id(challenge_test_id, is_deleted)
        mock_call_proc.assert_called_with("UpdateChallengeTestIsDeletedById", params=(challenge_test_id, is_deleted), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_update_challenge_comment_is_deleted_by_id(self, mock_call_proc):
        comment_id, is_deleted = 1, True
        result = SqlService.update_challenge_comment_is_deleted_by_id(comment_id, is_deleted)
        mock_call_proc.assert_called_with("UpdateChallengeCommentIsDeletedById", params=(comment_id, is_deleted), update=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_delete_challenge_by_id(self, mock_call_proc):
        challenge_id = 1
        result = SqlService.delete_challenge_by_id(challenge_id)
        mock_call_proc.assert_called_with("DeleteChallengeById", params=(challenge_id, ), delete=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_delete_challenge_test_by_id_and_challenge_id(self, mock_call_proc):
        challenge_test_id, challenge_id = 1, 2
        result = SqlService.delete_challenge_test_by_id_and_challenge_id(challenge_test_id, challenge_id)
        mock_call_proc.assert_called_with("DeleteChallengeTestByIdAndChallengeId", params=(challenge_test_id, challenge_id), delete=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_delete_challenge_comment_by_id_and_challenge_id(self, mock_call_proc):
        comment_id, challenge_id = 1, 2
        result = SqlService.delete_challenge_comment_by_id_and_challenge_id(comment_id, challenge_id)
        mock_call_proc.assert_called_with("DeleteChallengeCommentByIdAndChallengeId", params=(comment_id, challenge_id), delete=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_purge_account_by_username(self, mock_call_proc):
        username = 'testuser'
        result = SqlService.purge_account_by_username(username)
        mock_call_proc.assert_called_with("PurgeAccountByUsername", params=(username,), delete=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_purge_challenge_by_id(self, mock_call_proc):
        challenge_id = 1
        result = SqlService.purge_challenge_by_id(challenge_id)
        mock_call_proc.assert_called_with("PurgeChallengeById", params=(challenge_id,), delete=True)
        self.assertTrue(result)

    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_purge_challenge_test_by_id(self, mock_call_proc):
        challenge_test_id = 1
        result = SqlService.purge_challenge_test_by_id(challenge_test_id)
        mock_call_proc.assert_called_with("PurgeChallengeTestById", params=(challenge_test_id,), delete=True)
        self.assertTrue(result)
    
    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_purge_challenge_comment_by_id(self, mock_call_proc):
        challenge_comment_id = 1
        result = SqlService.purge_challenge_comment_by_id(challenge_comment_id)
        mock_call_proc.assert_called_with("PurgeChallengeCommentById", params=(challenge_comment_id,), delete=True)
        self.assertTrue(result)
    
    @patch('classes.util.sqlservice.SqlService.call_stored_procedure')
    def test_purge_challenge_submission_by_id(self, mock_call_proc):
        challenge_submission_id = 1
        result = SqlService.purge_challenge_submission_by_id(challenge_submission_id)
        mock_call_proc.assert_called_with("PurgeChallengeSubmissionById", params=(challenge_submission_id,), delete=True)
        self.assertTrue(result)


    



















