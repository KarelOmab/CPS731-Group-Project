from flask import Flask, render_template
import os
from dotenv import load_dotenv
from classes.util.sqlservice import SqlService

class App:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get("SECRET_KEY")
        
        # Routes setup
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/register', 'register', self.register)
        self.app.add_url_rule('/submit_registration', 'register_user', self.register_user, methods=['POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout)
        self.app.add_url_rule('/login', 'login', self.login)
        self.app.add_url_rule('/submit_login', 'submit_login', self.submit_login, methods=['POST'])
        self.app.add_url_rule('/challenges', 'challenges', self.challenges)
        self.app.add_url_rule('/insert_challenge', 'insert_challenge', self.insert_challenge)
        self.app.add_url_rule('/submit_challenge', 'submit_challenge', self.submit_challenge, methods=['POST'])
        self.app.add_url_rule('/submission/<int:challenge_id>', 'submission', self.submission, methods=['POST'])
        self.app.add_url_rule('/challenges/<int:challenge_id>', 'generic_challenge', self.generic_challenge, methods=['GET', 'POST'])
        self.app.add_url_rule('/submit_comment/<int:challenge_id>', 'submit_comment', self.submit_comment, methods=['POST'])
        self.app.add_url_rule('/delete_challenge/<int:challenge_id>', 'delete_challenge', self.delete_challenge)
        self.app.add_url_rule('/edit_challenge_name/<int:challenge_id>', 'edit_challenge_name', self.edit_challenge_name, methods=['POST'])
        self.app.add_url_rule('/edit_challenge_difficulty/<int:challenge_id>', 'edit_challenge_difficulty', self.edit_challenge_difficulty, methods=['POST'])
        self.app.add_url_rule('/edit_challenge_description/<int:challenge_id>', 'edit_challenge_description', self.edit_challenge_description, methods=['POST'])
        self.app.add_url_rule('/edit_challenge_stub-name/<int:challenge_id>', 'edit_challenge_stub_name', self.edit_challenge_stub_name, methods=['POST'])
        self.app.add_url_rule('/edit_challenge_stub-block/<int:challenge_id>', 'edit_challenge_stub_block', self.edit_challenge_stub_block, methods=['POST'])
        self.app.add_url_rule('/add_test_case/<int:challenge_id>', 'add_test_case', self.add_test_case, methods=['POST'])
        self.app.add_url_rule('/delete_test_case/<int:test_case_id>', 'delete_test_case', self.delete_test_case, methods=['POST'])
        self.app.add_url_rule('/delete_comment/<int:challenge_id>', 'delete_comment', self.delete_comment, methods=['POST'])

    def index(self):
        """
        Renders the home page of the website.

        Returns:
            A rendered template of 'index.html' which is the home page of the website.
        """
        return render_template('index.html')

    def register(self):
        """
        Renders the user registration page of the website.

        Returns:
            A rendered template of 'register.html' which is the page where new users can register an account.
        """
        pass

    def register_user(self):
        """
        Register a new user in the system.

        This method handles a POST request to register a new user by extracting 
        the username, password, and email from the request form. It uses the 
        CryptoService to hash the password before saving. The user's account details 
        are then inserted into the database via the SqlService.

        The USERGROUP_USER is set to a hardcoded value which defines the user group 
        for the new account.

        If the username or email is already in use, it sets an appropriate message.
        In case of a successful registration, a success message is communicated. 
        If an exception occurs during the process, it catches the exception and 
        returns a JSON response with success set to False and the error details, 
        with a 500 status code for server errors. If the request method is not POST,
        a 403 status code is returned indicating an unauthorized request.

        Returns:
            A rendered 'register.html' template with a message indicating the success
            or failure of the registration process.
        """
        pass

    def submit_login(self):
        """
        Process the login form submission and authenticate the user.

        This method retrieves the username and password from the submitted form data, 
        hashes the password using the CryptoService for secure comparison, and then 
        queries the database through SqlService to find a matching account.

        If a matching account is found, the user's session is populated with their 
        id, username, and privileged_mode status using Flask's session management. 
        The user is then redirected to the index page indicating a successful login.

        In case no account matches the provided credentials, the login fails, and 
        the method returns a plain text message indicating an invalid username or 
        password.

        Returns:
            A redirect to the 'index' route for a successful login, or a string 
            with an error message for a failed login attempt.
        """
        pass

    def logout(self):
        """
        Log out the current user.

        This method clears the current user's session by removing the user's id,
        username, and privileged_mode status from the session storage. It effectively
        signs the user out by discarding the session data that is associated with
        their current login.

        After clearing the session, the user is redirected to the index page which
        typically serves as the landing page after logout.

        Returns:
            A redirect to the 'index' route, which is the default page users see after logging out.
        """
        pass

    def login(self):
        """
        Render the login page template.

        This method returns the HTML content for the login page by rendering the
        'login.html' template. This is typically used to present the user with a
        login form.

        Returns:
            An HTML page rendered from the 'login.html' template.
        """
        pass

    def challenges(self):
        """
        Display all available challenges.

        This method fetches a list of all challenges from the database using the
        SqlService.get_all_challenges method. It then renders the 'challenges.html'
        template, passing the list of challenges to the template to be displayed to
        the user.

        Returns:
            An HTML page rendered from the 'challenges.html' template with all
            challenges passed as a context variable.
        """
        pass

    def insert_challenge(self):
        """
        Render the insert challenge page template.

        This method is used to display the HTML form for inserting a new challenge.
        It renders the 'insert_challenge.html' template which should contain the
        necessary form for a user to fill in and submit a new challenge.

        Returns:
            An HTML page rendered from the 'insert_challenge.html' template.
        """
        pass

    def submit_challenge(self):
        """
        Process the submission of a new challenge.

        This method handles the form submission for creating a new challenge. It collects
        the challenge details from the form, such as name, difficulty, description,
        code stub name and block, and time allowed for the challenge.

        Prior to insertion into the database, any necessary data validation should be
        performed. The method assumes the presence of the logged-in user's account ID in
        the session.

        It attempts to insert the new challenge into the database using the
        `SqlService.insert_challenge` function. If successful, it proceeds to insert the
        associated test cases using the `SqlService.insert_challenge_test` function.

        If the challenge is inserted correctly, a success message is flashed to the user.
        If inserting any test case fails, an error message is flashed instead. In the
        event of any exception, an error is flashed and logged.

        Returns:
            A redirect to the 'insert_challenge' route, potentially with flash messages
            indicating the status of the challenge creation (success or error).
        """
        pass

    def submission(self, challenge_id):
        """
        Process the submission of user code for a specific challenge.

        This method is responsible for handling the POST request when a user submits their code solution
        for a challenge. It checks for the validity of the request method, retrieves the submitted code
        from the form, fetches the associated challenge and its test cases from the database, and validates
        the user's code stub.

        If the challenge or tests do not exist, it aborts the request with a 404 status code or returns a
        501 status code with an appropriate message, respectively. It then validates the user code stub
        with the DockerService. If the validation fails, it returns a 400 status code with the validation
        message.

        Assuming validation passes, the DockerService is used to execute the user code against the challenge
        test cases. The execution results are then assessed to determine whether the user's solution passed
        all test cases.

        If the user's code passes all test cases, an attempt is made to insert the submission details into
        the database. A JSON response is returned to the user indicating success or failure of this operation,
        along with the execution time and character count.

        If the user's code fails any test case, or if an error, timeout, or exception occurs during code
        execution, a JSON response with the corresponding status code and details about the failure is returned.

        Parameters:
            challenge_id (int): The ID of the challenge for which the code is being submitted.

        Returns:
            A JSON response containing the result of the submission attempt, along with appropriate HTTP status
            codes. This response includes success messages, execution details, and error messages as applicable.
        """
        pass

    def generic_challenge(self, challenge_id):
        """
        Retrieve and display the details of a specific challenge.

        This method fetches the details of a given challenge, including its test cases and comments,
        from the database. It retrieves the challenge information by its ID, the associated test cases, 
        and any comments related to the challenge.

        If the user is logged in (indicated by the presence of 'id' in the session), it also fetches
        the user's submissions for this challenge. The submission data, if present, along with the
        challenge details, tests, and comments are then passed to the 'challenge.html' template for
        rendering.

        Parameters:
            challenge_id (int): The unique identifier of the challenge whose details are to be displayed.

        Returns:
            The 'challenge.html' template rendered with the challenge details, tests, comments, and user
            submission data (if the user is logged in and has submission data).
        """
        challenge_id = int(challenge_id)
        _challenge = SqlService.get_challenge_by_id(challenge_id)
        _tests = SqlService.get_challenge_tests_by_id_and_limit(challenge_id)
        _comments = SqlService.get_challenge_comments_by_id(challenge_id)
        challenge = {
            "name": _challenge.name,
            "difficulty": _challenge.difficulty,
            "description": _challenge.description,
        },
        tests = []
        for test in _tests:
            tests.append({
                "name": _challenge.stub_name,
                "input": test.test_input,
                "output": test.test_output,
            })
        comments = []
        for comment in _comments:
            comments.append({
                "title": comment.title,
                "username": comment.username,
                "text": comment.text,
                "datetime": comment.created_at,
            })
        return render_template('challenge.html', challenge=challenge, tests=tests, comments=comments)

    def submit_comment(self, challenge_id):
        """
        Submit a comment on a challenge by a logged-in user.

        This method processes the submission of a comment to a challenge, ensuring that the user is
        logged in (by checking the session for a user ID). The method attempts to retrieve the title
        and text of the comment from the form data. If either is missing, a flash message is generated
        and the user is redirected back to the challenge page.

        If the comment data is valid, the method calls the SqlService to insert the comment into the
        database. Depending on the result, it flashes a success or failure message and redirects to
        the challenge page.

        Parameters:
            challenge_id (int): The ID of the challenge for which the comment is being submitted.

        Returns:
            A redirect to the challenge page with a flash message indicating the outcome of the comment
            submission attempt.
        """
        pass
        

    def delete_challenge(self, challenge_id):
        """
        Delete a challenge from the database if the user has privileged access.

        This method checks if the user has 'privileged_mode' access within the session. If they do, it
        attempts to delete the challenge identified by challenge_id from the database. The method flashes
        a message to indicate whether the deletion was successful or failed due to an error or failed
        database operation.

        Parameters:
            challenge_id (int): The ID of the challenge to be deleted.

        Returns:
            A redirect to the challenges overview page with a flash message indicating the outcome of the
            deletion attempt.
        """
        pass

    def edit_challenge_name(self, challenge_id):
        """
        Edit the name of an existing challenge provided the user has the necessary privileges.

        This method allows a user with 'privileged_mode' access to edit the name of a challenge. It
        checks for 'privileged_mode' in the session and, if present, attempts to update the challenge
        name in the database using the new name provided in the form data.

        Parameters:
            challenge_id (int): The ID of the challenge for which the name is to be updated.

        Returns:
            A JSON response indicating success or failure of the update operation. If the user does not
            have the necessary permissions, it returns a 403 status code and a failure message.
        """
        pass

    def edit_challenge_difficulty(self, challenge_id):
         """
        Updates the difficulty level of a challenge if the user has the appropriate privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge to be edited.

        Returns:
            A JSON response indicating whether the update was successful, with an HTTP status code
            of 200 for success or 403 for permission denied. Flash messages provide user feedback.
        """
         pass

    def edit_challenge_description(self, challenge_id):
        """
        Edits the description of a challenge, given that the user has the necessary privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge to be edited.

        Returns:
            A JSON response indicating the outcome of the update with an HTTP status code of 200
            for success or 403 for permission denied. Flash messages provide feedback to the user.
        """
        pass

    def edit_challenge_stub_name(self, challenge_id):
        """
        Updates the stub name of a challenge if the user has privileged access.

        Parameters:
            challenge_id (int): The unique identifier for the challenge whose stub name is to be updated.

        Returns:
            A JSON response indicating the success status of the update, with an HTTP status code of 200
            for success or 403 for permission denied. Flash messages provide feedback on the action's outcome.
        """
        pass

    def edit_challenge_stub_block(self, challenge_id):
        """
        Edits the code stub (skeleton code) for a challenge if the user has administrative privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge whose stub is to be updated.

        Returns:
            A JSON response indicating success or failure of the update, with corresponding flash messages
            and an HTTP status code of 200 for success or 403 for permission denied.
        """
        pass

    def add_test_case(self, challenge_id):
        """
        Adds a new test case to a challenge if the user has the required privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge to which the test case will be added.

        Returns:
            A JSON response indicating whether the test case was successfully added, with an HTTP status code
            of 200 for success or 403 for permission denied. Flash messages provide user feedback.
        """
        pass

    def delete_test_case(self, challenge_id, test_case_id):
        """
        Deletes a test case from a challenge if the user has the necessary privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge.
            test_case_id (int): The unique identifier for the test case to be deleted.

        Returns:
            A JSON response indicating the success or failure of the deletion, with an HTTP status code of 200
            for success or 403 for permission denied. Flash messages provide feedback on the outcome.
        """
        pass

    def delete_comment(self, challenge_id, comment_id):
        """
        Deletes a comment from a challenge if the user has privileged access.

        Parameters:
            challenge_id (int): The unique identifier for the challenge.
            comment_id (int): The unique identifier for the comment to be deleted.

        Returns:
            A JSON response indicating the outcome of the deletion attempt, with an HTTP status code of 200
            for success or 403 for permission denied. Flash messages provide feedback to the user.
        """
        pass
        
    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == '__main__':
    my_app = App()
    my_app.run(debug=True)
    