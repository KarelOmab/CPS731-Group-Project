import unittest
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
        self.assertEqual(result, "Success")

        # Note receiving the message "Success" implies that the record was inserted
        # Additional cleanup code to remove the inserted data from the database
        SqlService.purge_account_by_username(username)  # purge this record

    def test_insert_account_fail_username_in_use(self):
            # Define test data
            usergroup = 2
            username = "karel"  #hash to guarantee uniqueness
            password = "testpassword123"
            email = "testuser@example.com"

            # Call the method
            result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

            # Assert that the result is as expected
            self.assertEqual(result, "Username in use")

    def test_insert_account_fail_email_in_use(self):
            # Define test data
            usergroup = 2
            username = "karel112"  #hash to guarantee uniqueness
            password = "testpassword123"
            email = "karel@email.com"

            # Call the method
            result = SqlService.insert_account(usergroup, username, password, email)[0]['message']

            # Assert that the result is as expected
            self.assertEqual(result, "Email in use")

    def test_insert_challenge_success(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "Easy"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)[0]['LAST_INSERT_ID()']

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNotNone(challenge_id)
        
        # Optionally: Verify the inserted data in the database
        challenge = SqlService.get_challenge_by_id(challenge_id)
        SqlService.purge_challenge_by_id(challenge_id)  # purge this record
        self.assertEqual(challenge.name, name)
        self.assertEqual(challenge.difficulty, difficulty)
        self.assertEqual(challenge.description, description)
        self.assertEqual(challenge.stub_name, stub_name)
        self.assertEqual(challenge.stub_block, stub_block)
        self.assertEqual(challenge.time_allowed_sec, time_allowed_sec)

        

    def test_insert_challenge_fail_missing_account_id(self):
        # Define test data
        account_id = None # karel
        name = None
        difficulty = "Easy"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_name(self):
        # Define test data
        account_id = 1 # karel
        name = None
        difficulty = "Easy"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_difficulty(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = None
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_invalid_difficulty(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_description(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = None
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_stub_name(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = None
        stub_block = "# TODO"
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_stub_block(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = None
        time_allowed_sec = 5.0

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_fail_missing_time_allowed_sec(self):
        # Define test data
        account_id = 1 # karel
        name = "Test Challenge" + "bd720e3aa2e89aff04e387d1baf40751c942fb5b290e08324a71dee07756dfb8"    #hash to guarantee uniqueness
        difficulty = "foobar"
        description = "This is a test challenge description."
        stub_name = "def foo(x)"
        stub_block = "# TODO"
        time_allowed_sec = None

        # Call the method
        challenge_id = SqlService.insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec)

        # Assert that None was returned (indicating failed insertion)
        self.assertIsNone(challenge_id)

    def test_insert_challenge_test_success(self):
        # Define test data
        challenge_id = 1  # Assuming this challenge ID exists in your test database
        input_data = "9, 10"
        output_data = "19"

        # Call the method
        challenge_test_id = SqlService.insert_challenge_test(challenge_id, input_data, output_data)[0]['LAST_INSERT_ID()']

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNotNone(challenge_test_id)

        # Optionally: Verify the inserted data in the database
        challenge_test = SqlService.get_challenge_test_by_id(challenge_test_id)
        SqlService.purge_challenge_test_by_id(challenge_id)  # purge this record
        self.assertEqual(challenge_test.test_input, input_data)
        self.assertEqual(challenge_test.test_output, output_data)

    def test_insert_challenge_test_fail_missing_input(self):
        # Define test data
        challenge_id = 1  # Assuming this challenge ID exists in your test database
        input_data = None
        output_data = "19"

        # Call the method
        challenge_test_id = SqlService.insert_challenge_test(challenge_id, input_data, output_data)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(challenge_test_id)

    def test_insert_challenge_test_fail_missing_output(self):
        # Define test data
        challenge_id = 1  # Assuming this challenge ID exists in your test database
        input_data = "9, 10"
        output_data = None

        # Call the method
        challenge_test_id = SqlService.insert_challenge_test(challenge_id, input_data, output_data)

        # Assert that an ID was returned (indicating successful insertion)
        self.assertIsNone(challenge_test_id)


        

    

    

# This block runs the test suite
if __name__ == '__main__':
    unittest.main()