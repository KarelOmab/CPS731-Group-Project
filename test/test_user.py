import unittest
from classes.account.user import User

class TestUser(unittest.TestCase):
    
    def setUp(self):
        # Setup a User object before each test
        self.user = User(id=2, username='bob')

    def test_constructor(self):
        # Test that the constructor correctly initializes the object
        self.assertEqual(self.user.id, 2)
        self.assertEqual(self.user.username, 'bob')

    def test_id_getter(self):
        # Test the id getter
        self.assertEqual(self.user.id, 2)

    def test_username_getter(self):
        # Test the username getter
        self.assertEqual(self.user.username, 'bob')

    def test_privileged_mode(self):
        # Test the privileged_mode property
        self.assertFalse(self.user.privileged_mode)

    def test_str_representation(self):
        # Test the string representation of the user object
        expected_str = "id:2, username:bob, privileged_mode:False"
        self.assertEqual(str(self.user), expected_str)

if __name__ == '__main__':
    unittest.main()