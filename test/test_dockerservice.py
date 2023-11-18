import unittest
from classes.util.dockerservice import DockerService

class TestDockerService(unittest.TestCase):
    
    def test_validate_user_method_valid(self):
        code = "def sum(x, y): return x + y"
        result, message = DockerService.validate_user_method(code, 'sum')
        self.assertTrue(result)
        self.assertEqual(message, "valid")

    def test_validate_user_method_invalid(self):
        code = "def summm(x, y): return x + y"
        result, message = DockerService.validate_user_method(code, 'sum')
        self.assertFalse(result)
        self.assertEqual("Error! Your code must contain the required method: def sum", message)

if __name__ == '__main__':
    unittest.main()