import unittest
from datetime import datetime
from classes.challenge.challenge import Challenge

class TestChallenge(unittest.TestCase):
    def setUp(self):
        # Setting up a Challenge object before each test
        self.challenge = Challenge(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            name="Some Challenge Name",
            difficulty="Easy",
            description="Some Challenge Description",
            stub_name="def foo(x, y)",
            stub_block="# TODO",
            time_allowed_sec=5
        )

    def test_id_getter_setter(self):
        # Test the id getter and setter
        self.challenge.id = 1
        self.assertEqual(self.challenge.id, 1)

    def test_created_at_getter_setter(self):
        # Test the created_at getter and setter
        new_time = datetime.now()
        self.challenge.created_at = new_time
        self.assertEqual(self.challenge.created_at, new_time)

    def test_account_id_getter_setter(self):
        # Test the account_id getter and setter
        self.challenge.account_id = 1
        self.assertEqual(self.challenge.account_id, 1)

    def test_is_deleted_getter_setter(self):
        # Test the is_deleted getter and setter
        self.challenge.is_deleted = True
        self.assertTrue(self.challenge.is_deleted)

    def test_name_getter_setter(self):
        # Test the name getter and setter
        self.challenge.name = "New Challenge Name"
        self.assertEqual(self.challenge.name, "New Challenge Name")

    def test_difficulty_getter_setter(self):
        # Test the difficulty getter and setter
        self.challenge.difficulty = "Hard"
        self.assertEqual(self.challenge.difficulty, "Hard")

    def test_description_getter_setter(self):
        # Test the description getter and setter
        self.challenge.description = "New Description"
        self.assertEqual(self.challenge.description, "New Description")

    def test_stub_name_getter_setter(self):
        # Test the stub_name getter and setter
        self.challenge.stub_name = "def bar(a, b)"
        self.assertEqual(self.challenge.stub_name, "def bar(a, b)")

    def test_stub_block_getter_setter(self):
        # Test the stub_block getter and setter
        self.challenge.stub_block = "# PUT YOUR CODE HERE"
        self.assertEqual(self.challenge.stub_block, "# PUT YOUR CODE HERE")

    def test_time_allowed_sec_getter_setter(self):
        # Test the time_allowed_sec getter and setter
        self.challenge.time_allowed_sec = 7
        self.assertEqual(self.challenge.time_allowed_sec, 7)

    def test_challenge_tests_getter_setter(self):
        # Test the challenge_tests getter and setter
        self.challenge.challenge_tests = ["test1", "test2"]
        self.assertListEqual(self.challenge.challenge_tests, ["test1", "test2"])

if __name__ == '__main__':
    unittest.main()