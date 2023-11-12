import unittest
from classes.util.cryptoservice import CryptoService # this is my import to test 

# This is the test class
class TestMyClass(unittest.TestCase):
    
    def setUp(self):
        # Set up any variables or instances needed for the tests
        #self.my_class_instance = MyClass()
        pass

    def test_my_password_hashing_success(self):
        # This is the test case for 'my_function' of MyClass
        self.assertTrue(CryptoService.hash_password("123456") == "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
       
    def test_my_password_hashing_success(self):
        # This is the test case for 'my_function' of MyClass
        self.assertFalse(CryptoService.hash_password("123456") == "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c89")

# This block runs the test suite
if __name__ == '__main__':
    unittest.main()