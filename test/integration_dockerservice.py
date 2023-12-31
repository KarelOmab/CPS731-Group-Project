import unittest
from datetime import datetime

import sys
import os

# Add the parent directory to the PYTHONPATH so the App class can be imported
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from classes.util.dockerservice import DockerService
from classes.challenge.challenge import Challenge
from classes.challenge.challengetest import ChallengeTest

class TestDockerServiceIntegration(unittest.TestCase):

    def test_execute_code_success(self):
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
        
        # Simulate test cases
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

        # Sample user code that should be executed inside Docker
        user_code = """
def sum(x, y):
    return x + y
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], len(tests))
        self.assertEqual(result['success'], True)
        self.assertEqual(result['timeout'], False)

    def test_execute_code_success_print_statements(self):
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
        
        # Simulate test cases
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

        # Sample user code that should be executed inside Docker
        user_code = """
def sum(x, y):
    print(x, y)
    return x + y
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], len(tests))
        self.assertEqual(result['success'], True)
        self.assertEqual(result['timeout'], False)
        self.assertEqual(result['print_outputs'], ['6 12', '4 7'])

    def test_execute_code_fail_invalid_result(self):
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
        
        # Simulate test cases
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

        # Sample user code that should be executed inside Docker
        user_code = """
def sum(x, y):
    return x + x
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)

    def test_execute_code_fail_syntax_error(self):
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
        
        # Simulate test cases
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

        # Sample user code that should be executed inside Docker
        user_code = """
def sum(x, y):
    ret x + y
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['exception'], "SyntaxError: invalid syntax")

    def test_execute_code_fail_timeout(self):
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
            time_allowed_sec=10
        )
        
        # Simulate test cases
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

        # Sample user code that should be executed inside Docker
        user_code = """
def sum(x, y):
    while True: x = 1
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['timeout'], True)

if __name__ == '__main__':
    unittest.main()
