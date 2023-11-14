import unittest
from classes.util.cryptoservice import CryptoService

class TestMyClass(unittest.TestCase):
    
    def test_my_password_hashing_success(self):
        self.assertTrue(CryptoService.hash_password("123456") == "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
       
    def test_my_password_hashing_fail(self):
        self.assertFalse(CryptoService.hash_password("123456") == "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c89")

if __name__ == '__main__':
    unittest.main()