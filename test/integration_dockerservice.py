import unittest
from datetime import datetime
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
    ret x + x
"""

        # Run the execute_code method
        result = DockerService.execute_code(challenge, tests, user_code)

        # Assertions to validate the behavior
        self.assertEqual(result['tests_total'], len(tests))
        self.assertEqual(result['tests_passed'], 0)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['exception'], "SyntaxError: invalid syntax")

if __name__ == '__main__':
    unittest.main()
