import ast
import threading
import time
import re
import docker

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
        client = docker.from_env()
        appended_code_base = f"""
def captured_print(*args, **kwargs):
    global print_outputs
    original_print(*args, **kwargs)
    print_outputs.append(' '.join(map(str, args)))

import builtins
original_print = builtins.print
builtins.print = captured_print
print_outputs = []

""" + user_code

        def target(result_dict):
            container = client.containers.run(
                "safe-python-env",
                command=["sleep", "300"],
                detach=True,
                network_mode="none",
                mem_limit='100m',
                cpuset_cpus='0',
                read_only=True
            )

            start_time = time.time()

            for test_case in tests:
                appended_code = appended_code_base + f"\nresult = {challenge.stub_name}({test_case.test_input})\nprint('RESULT:', result)\n"

                try:
                    output = container.exec_run(
                        ["python", "-c", appended_code]
                    )[1]  # Using exec_run to execute the command on the already running container
                    lines = output.decode().strip().splitlines()
                    function_result = None

                    for line in lines:
                        if line.startswith("RESULT:"):
                            function_result_str = line.split(":", 1)[1].strip()
                            # Safely evaluate the string to get the actual list
                            function_result = ast.literal_eval(function_result_str)
                        else:
                            # Using regex to find the specific error message
                            match = re.search(r"(\w+Error): ([^\n]+)", line)
                            if match:
                                error_type, error_detail = match.groups()
                                result_dict['exception'] = f"{error_type}: {error_detail}"
                                result_dict['success'] = False
                            else:
                                result_dict['print_outputs'].append(line)

                    # Compare the evaluated list with the expected result
                    if function_result != ast.literal_eval(test_case.test_output):
                        result_dict['error'] = f"Failed! For input ({test_case.test_input}) expected result {test_case.test_output}, but returned {function_result}."
                        result_dict['success'] = False
                        return  # Terminate upon first unexpected result
                    else:
                        result_dict['tests_passed'] += 1
                except docker.errors.ContainerError as ce:
                    error_message = ce.stderr.decode()
                    print("error_message", error_message)

                    # Using regex to find the specific error message
                    match = re.search(r"(\w+Error): ([^\n]+)", error_message)
                    if match:
                        error_type, error_detail = match.groups()
                        result_dict['exception'] = f"{error_type}: {error_detail}"
                        result_dict['success'] = False

            result_dict['exec_time'] = time.time() - start_time
            container.stop()  # Stop the container
            container.remove()  # Remove the container

        result_dict = {
            'tests_total': len(tests),
            'tests_passed': 0,
            'print_outputs': [],
            'error': "",
            'exception': "",
            'success': True,
            'timeout': False,
            'exec_time': 0.0,
            'exec_chars': 0
        }
        thread = threading.Thread(target=target, args=(result_dict,))
        thread.start()
        thread.join(timeout=challenge.time_allowed_sec)
        result_dict['exec_chars'] = len(user_code)

        if thread.is_alive():
            result_dict['timeout'] = (result_dict['exec_time'] >= challenge.time_allowed_sec)
            result_dict['success'] = False

        return result_dict
