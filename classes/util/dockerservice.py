import ast
class DockerService:
    @staticmethod
    def validate_user_method(code, method_name):
        """
        Validates if the provided code snippet defines a method with the specified name.

        The method parses the given code to check for the existence of a function definition
        that matches the 'method_name' provided. This is done using the 'ast' module which
        allows the code to be treated as a tree of objects that can be traversed to find
        specific elements like function definitions.

        Args:
            code (str): A string containing the user's code snippet to be validated.
            method_name (str): The name of the method that should be defined in the code.

        Returns:
            tuple: A tuple containing a boolean and a message. The boolean is True if the
                method is defined, False otherwise. The message is 'valid' if the method
                is found, or an error message specifying that the required method is missing.
        """
        try:
            tree = ast.parse(code)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    if node.name == method_name:
                        return True, "valid"
            return False, f"Error! Your code must contain the required method: def {method_name}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def execute_code(challenge, tests, user_code):
        """
        Executes a user's code against a set of test cases inside a secure Docker environment.

        The method appends the user's code with a custom print function to capture the outputs.
        It then runs each test case input through the user-defined function within the code
        and compares the output against the expected result. The execution happens inside a
        Docker container to ensure security and isolation from the host environment.

        Args:
            challenge (Challenge): An object representing the challenge including metadata like the stub name and timeout.
            tests (list): A list of test cases, each with 'test_input' and 'test_output' attributes.
            user_code (str): The user's code that defines the function to test.

        Returns:
            dict: A dictionary containing the results of the code execution, including:
                - The total number of tests and how many passed.
                - Captured print outputs.
                - Any error or exception messages.
                - Execution time and a flag indicating if the execution timed out.
        """
        pass
