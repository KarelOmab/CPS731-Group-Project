import unittest
from datetime import datetime
from classes.challenge.challengesubmission import ChallengeSubmission

class TestChallengeSubmission(unittest.TestCase):
    def setUp(self):
        # Setting up a ChallengeSubmission object before each test
        self.submission = ChallengeSubmission(
            id=1,
            created_at=datetime.now(),
            challenge_id=1,
            account_id=1,
            exec_time=2.5,
            exec_chars=25,
            exec_src="def sum(x, y): return x + y"
        )

    def test_id_getter_setter(self):
        # Test the id getter and setter
        self.submission.id = 1
        self.assertEqual(self.submission.id, 1)

    def test_created_at_getter_setter(self):
        # Test the created_at getter and setter
        new_time = datetime.now()
        self.submission.created_at = new_time
        self.assertEqual(self.submission.created_at, new_time)

    def test_challenge_id_getter_setter(self):
        # Test the challenge_id getter and setter
        self.submission.challenge_id = 1
        self.assertEqual(self.submission.challenge_id, 1)

    def test_account_id_getter_setter(self):
        # Test the account_id getter and setter
        self.submission.account_id = 1
        self.assertEqual(self.submission.account_id, 1)

    def test_exec_time_getter_setter(self):
        # Test the exec_time getter and setter
        self.submission.exec_time = 1.0
        self.assertEqual(self.submission.exec_time, 1.0)

    def test_exec_chars_getter_setter(self):
        # Test the exec_chars getter and setter
        self.submission.exec_chars = 1
        self.assertEqual(self.submission.exec_chars, 1)

    def test_exec_src_getter_setter(self):
        # Test the exec_src getter and setter
        self.submission.exec_src = "def foo(x, y): pass"
        self.assertEqual(self.submission.exec_src, "def foo(x, y): pass")

if __name__ == '__main__':
    unittest.main()