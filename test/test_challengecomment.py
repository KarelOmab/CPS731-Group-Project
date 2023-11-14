import unittest
from datetime import datetime
from classes.challenge.challengecomment import ChallengeComment

class TestChallengeComment(unittest.TestCase):
    def setUp(self):
        # Setting up a ChallengeComment object before each test
        self.comment = ChallengeComment(
            id=1,
            created_at=datetime.now(),
            account_id=1,
            is_deleted=False,
            challenge_id=1,
            title="Test Comment Title",
            text="Test Comment Text",
            username="some_username"
        )

    def test_id_getter_setter(self):
        # Test the id getter and setter
        self.comment.id = 1
        self.assertEqual(self.comment.id, 1)

    def test_created_at_getter_setter(self):
        # Test the created_at getter and setter
        new_time = datetime.now()
        self.comment.created_at = new_time
        self.assertEqual(self.comment.created_at, new_time)

    def test_account_id_getter_setter(self):
        # Test the account_id getter and setter
        self.comment.account_id = 1
        self.assertEqual(self.comment.account_id, 1)

    def test_is_deleted_getter_setter(self):
        # Test the is_deleted getter and setter
        self.comment.is_deleted = True
        self.assertTrue(self.comment.is_deleted)

    def test_challenge_id_getter_setter(self):
        # Test the challenge_id getter and setter
        self.comment.challenge_id = 1
        self.assertEqual(self.comment.challenge_id, 1)

    def test_title_getter_setter(self):
        # Test the title getter and setter
        self.comment.title = "New Title"
        self.assertEqual(self.comment.title, "New Title")

    def test_text_getter_setter(self):
        # Test the text getter and setter
        self.comment.text = "New Text"
        self.assertEqual(self.comment.text, "New Text")

    def test_username_getter_setter(self):
        # Test the username getter and setter
        self.comment.username = "new_user"
        self.assertEqual(self.comment.username, "new_user")

if __name__ == '__main__':
    unittest.main()