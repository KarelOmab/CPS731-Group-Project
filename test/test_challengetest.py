import unittest
from datetime import datetime
from classes.challenge.challengetest import ChallengeTest

class TestChallengeTest(unittest.TestCase):
    def setUp(self):
        # Setting up a ChallengeTest object before each test
        self.challenge_test = ChallengeTest(
            id=1,
            challenge_id=1,
            is_deleted=False,
            test_input="6, 12",
            test_output="18"
        )

    def test_id_getter_setter(self):
        # Test the id getter and setter
        self.challenge_test.id = 1
        self.assertEqual(self.challenge_test.id, 1)

    def test_challenge_id_getter_setter(self):
        # Test the challenge_id getter and setter
        self.challenge_test.challenge_id = 1
        self.assertEqual(self.challenge_test.challenge_id, 1)

    def test_is_deleted_getter_setter(self):
        # Test the is_deleted getter and setter
        self.challenge_test.is_deleted = True
        self.assertTrue(self.challenge_test.is_deleted)

    def test_test_input_getter_setter(self):
        # Test the test_input getter and setter
        self.challenge_test.test_input = "5, 6"
        self.assertEqual(self.challenge_test.test_input, "5, 6")

    def test_test_output_getter_setter(self):
        # Test the test_output getter and setter
        self.challenge_test.test_output = "11"
        self.assertEqual(self.challenge_test.test_output, "11")

if __name__ == '__main__':
    unittest.main()