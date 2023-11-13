import unittest
from unittest.mock import patch, MagicMock
from classes.util.cryptoservice import CryptoService # this is my import to test
from classes.util.sqlservice import SqlService

# This is the test class
class TestMyClass(unittest.TestCase):
    
    def setUp(self):
        # Set up any variables or instances needed for the tests
        #self.my_class_instance = MyClass()
        pass

    def test_my_password_hashing_success(self):
        self.assertTrue(CryptoService.hash_password("123456") == "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
       
    def test_my_password_hashing_fail(self):
        self.assertFalse(CryptoService.hash_password("123456") == "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c89")

    def test_insert_account_success(self):
        # Define test data
        usergroup = 3
        username = "testuser" + "ae5deb822e0d71992900471a7199d0d95b8e7c9d05c40a8245a281fd2c1d6684"  #hash to guarantee uniqueness
        password = "testpassword123"
        email = "testuser@example.com"

        # Call the method
        result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

        # Assert that the result is as expected
        self.assertEquals(result, "Success")

        # Additional cleanup code to remove the inserted data from the database
        SqlService.purge_account_by_username(username)

    def test_insert_account_username_in_use(self):
            # Define test data
            usergroup = 2
            username = "karel"  #hash to guarantee uniqueness
            password = "testpassword123"
            email = "testuser@example.com"

            # Call the method
            result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

            # Assert that the result is as expected
            self.assertEquals(result, "Username in use")

    def test_insert_account_email_in_use(self):
            # Define test data
            usergroup = 2
            username = "karel112"  #hash to guarantee uniqueness
            password = "testpassword123"
            email = "karel@email.com"

            # Call the method
            result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

            # Assert that the result is as expected
            self.assertEquals(result, "Email in use")

    

    

# This block runs the test suite
if __name__ == '__main__':
    unittest.main()