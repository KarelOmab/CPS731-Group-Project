import unittest
from classes.account.moderator import Moderator

class TestModerator(unittest.TestCase):
    
    def setUp(self):
        self.moderator = Moderator(id=1, username='moderator')

    def test_id(self):
        self.assertEqual(self.moderator.id, 1)

    def test_username(self):
        self.assertEqual(self.moderator.username, 'moderator')

    def test_privileged_mode(self):
        self.assertTrue(self.moderator.privileged_mode)

    def test_str_representation(self):
        expected_str = "id:1, username:moderator, privileged_mode:True"
        self.assertEqual(str(self.moderator), expected_str)