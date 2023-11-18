import unittest
from classes.util.dockerservice import DockerService
from datetime import datetime
from unittest.mock import patch, MagicMock
from classes.challenge.challenge import Challenge
from classes.challenge.challengetest import ChallengeTest
from io import StringIO
import docker

# The purpose of these mock tests is to do line coverage
# These testers simply test line execution
# We have a separate integration test file for actual (real data) processing

class TestDockerService(unittest.TestCase):
    
    def test_validate_user_method_valid(self):
        code = "def sum(x, y): return x + y"
        result, message = DockerService.validate_user_method(code, 'sum')
        self.assertTrue(result)
        self.assertEqual(message, "valid")

    def test_validate_user_method_invalid(self):
        code = "def summm(x, y): return x + y"
        result, message = DockerService.validate_user_method(code, 'sum')
        self.assertFalse(result)
        self.assertEqual("Error! Your code must contain the required method: def sum", message)

    def test_validate_user_method_exception(self):
        invalid_code = "Hello World"
        result = DockerService.validate_user_method(invalid_code, "sum")
        self.assertFalse(result[0])

    @patch('docker.from_env')
    def test_execute_code_fail_invalid_result(self, mock_docker):
        # Setup a mock for the Docker client and container
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_docker.return_value = mock_client
        mock_client.containers.run.return_value = mock_container

        # Set up a mock return value for container's exec_run method to simulate code execution with invalid results
        # The user code returns x + x, so for input "6, 12" it should return "12" (incorrect result)
        mock_output = b"RESULT: 12\nRESULT: 8"  # Incorrect results according to user code
        mock_container.exec_run.return_value = (0, mock_output)  # Simulate exec_run returning a tuple with exit status and output

        # Define the Challenge and ChallengeTest instances
        challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Test Sum",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="sum",
            stub_block="# TODO",
            time_allowed_sec=20
        )

        tests = [
            ChallengeTest(
                id=1,
                challenge_id=1,
                is_deleted=False,
                test_input="6, 12",
                test_output="18"
            ),
            ChallengeTest(
                id=2,
                challenge_id=1,
                is_deleted=False,
                test_input="4, 7",
                test_output="11"
            )
        ]

        # Sample user code
        user_code = """
def sum(x, y):
    return x + x  # Incorrect implementation
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)

    @patch('docker.from_env')
    def test_execute_code_fail_syntax_error(self, mock_docker):
        # Setup a mock for the Docker client and container
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_docker.return_value = mock_client
        mock_client.containers.run.return_value = mock_container

        # Set up a mock return value for container's exec_run method to simulate a syntax error
        mock_output = b"SyntaxError: invalid syntax"
        mock_container.exec_run.return_value = (1, mock_output)  # Simulate exec_run returning a tuple with exit status and error output

        # Define the Challenge and ChallengeTest instances
        challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Test Sum",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="sum",
            stub_block="# TODO",
            time_allowed_sec=20
        )

        tests = [
            ChallengeTest(
                id=1,
                challenge_id=1,
                is_deleted=False,
                test_input="6, 12",
                test_output="18"
            ),
            ChallengeTest(
                id=2,
                challenge_id=1,
                is_deleted=False,
                test_input="4, 7",
                test_output="11"
            )
        ]

        # Sample user code with a syntax error
        user_code = """
def sum(x, y):
    ret x + y  # Syntax error
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['exception'], "SyntaxError: invalid syntax")

    @patch('docker.from_env')
    @patch('threading.Thread')
    def test_execute_code_fail_timeout(self, mock_thread, mock_docker):
        # Setup a mock for the Docker client and container
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_docker.return_value = mock_client
        mock_client.containers.run.return_value = mock_container

        # Mock the behavior of the threading.Thread to simulate a timeout
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        mock_thread_instance.is_alive.return_value = True  # Simulate the thread still being alive after timeout

        # Define the Challenge and ChallengeTest instances
        challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Test Sum",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="sum",
            stub_block="# TODO",
            time_allowed_sec=10  # Set a short timeout
        )

        tests = [
            ChallengeTest(
                id=1,
                challenge_id=1,
                is_deleted=False,
                test_input="6, 12",
                test_output="18"
            ),
            ChallengeTest(
                id=2,
                challenge_id=1,
                is_deleted=False,
                test_input="4, 7",
                test_output="11"
            )
        ]

        # Sample user code that simulates an infinite loop
        user_code = """
def sum(x, y):
    while True: x = 1  # Infinite loop
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['timeout'], True)


    @patch('docker.from_env')
    @patch('sys.stdout', new_callable=StringIO)  # Redirect stdout
    def test_execute_code_container_error(self, mock_stdout, mock_docker):
        # Setup a mock for the Docker client and container
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_docker.return_value = mock_client
        mock_client.containers.run.return_value = mock_container

        # Simulate a ContainerError with stderr as bytes
        mock_container.exec_run.side_effect = docker.errors.ContainerError(
            container=mock_container,
            exit_status=1,
            command="python -c 'code'",
            image="python:3.11",
            stderr=b"TestError: simulated container error"
        )

        challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Some Challenge Name",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="def foo(x, y)",
            stub_block="# TODO",
            time_allowed_sec=20
        )
        tests = [ChallengeTest(
            id=1,
            challenge_id=1,
            is_deleted=False,
            test_input="6, 12",
            test_output="18"
        )]
        user_code = 'print("hello world")'

        result = DockerService.execute_code(challenge, tests, user_code)

        # Assert that the exception was caught and handled correctly
        self.assertIn('TestError: simulated container error', result['exception'])
        self.assertFalse(result['success'])

    @patch('docker.from_env')
    def test_execute_code_capture_prints(self, mock_docker_env):
        # Setup mock Docker container and its exec_run return value
        mock_container = MagicMock()
        mock_container.exec_run.return_value = (0, b'Hello World\nRESULT: True')
        mock_docker_env.return_value.containers.run.return_value = mock_container

        # Dummy challenge and tests
        challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Some Challenge Name",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="def foo(x, y)",
            stub_block="# TODO",
            time_allowed_sec=20
        )
        tests = [ChallengeTest(
            id=1,
            challenge_id=1,
            is_deleted=False,
            test_input="6, 12",
            test_output="18"
        )]

        # Call execute_code
        user_code = "print('Hello World')"
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions
        self.assertIn('Hello World', result['print_outputs'])

    @patch('docker.from_env')
    def test_execute_code_passed_tests(self, mock_docker_env):
        # Setup mock Docker container and its exec_run return value
        mock_container = MagicMock()
        mock_container.exec_run.return_value = (0, b'RESULT: 18')
        mock_docker_env.return_value.containers.run.return_value = mock_container

        # Dummy challenge and tests
        challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Some Challenge Name",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="def foo(x, y)",
            stub_block="# TODO",
            time_allowed_sec=20
        )
        tests = [ChallengeTest(
            id=1,
            challenge_id=1,
            is_deleted=False,
            test_input="6, 12",
            test_output="18"
        )]

        # Call execute_code
        user_code = "def foo(x, y):\n  return 18"
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions
        self.assertEqual(result['tests_passed'], 1)

        

if __name__ == '__main__':
    unittest.main()