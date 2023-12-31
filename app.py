from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, abort
from flask import request, redirect, url_for
from dotenv import load_dotenv
from classes.util.sqlservice import SqlService
from classes.util.cryptoservice import CryptoService
from classes.util.dockerservice import DockerService

class App:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.secret_key = 'dasdsahdkjsadhasjkhjkdhsajkd'
        
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
        self.app.add_url_rule('/sort_challenges/<sorting_criteria>', 'sort_challenges', self.sort_challenges, methods=['POST'])
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
        self.app.add_url_rule('/delete_test_case/<int:challenge_id>/<int:test_case_id>', 'delete_test_case', self.delete_test_case, methods=['POST'])
        self.app.add_url_rule('/delete_comment/<int:challenge_id>/<int:comment_id>', 'delete_comment', self.delete_comment, methods=['POST'])

    def index(self):
        """
        Renders the home page of the website.

        Returns:
            A rendered template of 'index.html' which is the home page of the website.
        """
        session['sorting_criteria'] = 'difficulty'
        return render_template('index.html')

    def register(self):
        """
        Renders the user registration page of the website.

        Returns:
            A rendered template of 'register.html' which is the page where new users can register an account.
        """
        return render_template('register.html')
    
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

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email_address')

            if not all([email, username, password]):
                return render_template('register.html', error_message='Please fill all fields')

            hashed_password = CryptoService.hash_password(password)
            
            try:
                # insert the account into the database
                USERGROUP_USER = 3  #hardcoded here for now
                result = SqlService.insert_account(usergroup=USERGROUP_USER, username=username, password=hashed_password, email=email)
                result_message = result[0]['message']
                # Check the result and display appropriate message
                if result_message == 'Success':
                    return render_template('register.html', success_message='Registration successful')
                elif result_message == 'Username in use':
                    return render_template('register.html', error_message='Username already in use'), 400
                elif result_message == 'Email in use':
                    return render_template('register.html', error_message='Email already in use'), 400
            except Exception as e:
            # Handle other exceptions (e.g., database connection issues)
                return render_template('register.html', error_message='An error occurred while registering - please try again later'), 500
        return redirect(url_for('register')), 403  # 403 Forbidden
            
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
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not all([username, password]):
                return render_template('login.html', error_message='Please enter both username and password')

            hashed_password = CryptoService.hash_password(password)

            try:
                # Retrieve account from the database based on username and hashed password
                account = SqlService.get_account_by_username_password(username, hashed_password)

                if account:
                    # Populate user's session with relevant information
                    session['user_id'] = account.id
                    session['username'] = account.username
                    session['privileged_mode'] = account.privileged_mode

                    # Redirect to the index page after successful login
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error_message='Invalid username or password')
            except Exception as e:
                # Handle other exceptions (e.g., database connection issues)
                return render_template('login.html', error_message='An error occurred during login - please try again later')

        # If the request method is not POST, redirect to the login page
        return redirect(url_for('login'))

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
        session.clear()
        return redirect(url_for('index'))

    def login(self):
        """
        Render the login page template.

        This method returns the HTML content for the login page by rendering the
        'login.html' template. This is typically used to present the user with a
        login form.

        Returns:
            An HTML page rendered from the 'login.html' template.
        """
        return render_template('login.html')

    def sort_challenges(self,sorting_criteria):
        """
            whenn the user selects how the challenges displayed to be sorted, we want
            set a session variable to, and redirect to the challenge page so that the 
            challenges are displayed based on the new user sorting_criteria
        """
        session['sorting_criteria'] = sorting_criteria
        return redirect(url_for('challenges'))
    
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

        #fetch all the challenges
        challenges = SqlService.get_all_challenges()

        #Sort the challenges by name
        if( session['sorting_criteria'] == 'name'):
            challenges = sorted(challenges, key=lambda x: x.name)
            
        #Sorting the challenges by their difficulty level
        else:
            difficulty_mapping = {'Easy': 1, 'Medium': 2, 'Hard': 3}
            challenges.sort(key=lambda x: difficulty_mapping.get(x.difficulty, 0))

        return render_template("challenges.html", challenges = challenges)

    def insert_challenge(self):
        """
        Render the insert challenge page template.

        This method is used to display the HTML form for inserting a new challenge.
        It renders the 'insert_challenge.html' template which should contain the
        necessary form for a user to fill in and submit a new challenge.

        Returns:
            An HTML page rendered from the 'insert_challenge.html' template.
        """
        return render_template("insert_challenge.html")

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

        # Access the new challenge informations
        challenge_name = request.form['challengeName']
        challenge_difficulty = request.form['challengeDifficulty']
        challenge_description = request.form['challengeDescription']
        stub_name = request.form['stubName']
        stub_block = request.form['stubBlock']
        time_allowed = request.form['timeAllowed']

        # For the dynamic test cases, you might use a prefix and loop over them
      
        input_test_cases = request.form.getlist('inputParameters[]')
        output_test_cases = request.form.getlist('expectedOutput[]')
       
        # Process the new challenge to the database
        try:
            if session['privileged_mode']:
                last_id = SqlService.insert_challenge(session['user_id'],challenge_name,challenge_difficulty, challenge_description, stub_name, stub_block,time_allowed)

                #inserting a challenge test cases
                for input_case, output_case in zip(input_test_cases,output_test_cases):
                    last_id_inserted = SqlService.insert_challenge_test(last_id[0]['LAST_INSERT_ID()'],input_case,output_case)
            
                if last_id != None:
                    challenges = SqlService.get_all_challenges()

        except RuntimeError as err:
            print(f"Error! {err}")

        return redirect(url_for('challenges'))
    

    def submission(self, challenge_id):
        
        if request.method != 'POST':
            abort(405)

        user_code = request.form.get('stub-block')
  
        # Retrieve challenge and test data from database
        challenge = SqlService.get_challenge_by_id(challenge_id)
        tests = SqlService.get_challenge_tests_by_id(challenge_id)

        if not challenge:
            abort(404)  # Challenge not found

        if not tests:
            return jsonify(
                message="System error: Test Cases Not Implemented. Please come back later!",
                flash={"message": "Test cases are not implemented yet.", "category": "error"}
            ), 501

        stub_valid_result, msg = DockerService.validate_user_method(user_code, challenge.stub_name)
        if not stub_valid_result:
            return jsonify(
                message=stub_valid_result,
                flash={"message": msg, "category": "error"}
            ), 400

        result_dict = DockerService.execute_code(challenge, tests, user_code)
        output_str = "\n".join(result_dict['print_outputs'])

        if result_dict['tests_passed'] == result_dict['tests_total']:
            try:
                result = SqlService.insert_challenge_submission(challenge_id, session['user_id'], result_dict['exec_time'], result_dict['exec_chars'], user_code)

                if result:
                    return jsonify(
                        message="Correct! Your function returned the expected results for all test cases.",
                        flash={"message": "Submission added successfully!", "category": "success"},
                        printout=output_str,
                        exec_time=result_dict['exec_time'],
                        exec_chars=result_dict['exec_chars']
                    ), 200
                else:
                    return jsonify(
                        message="Failed to add your submission.",
                        printout=output_str,
                        flash={"message": "Failed to add submission.", "category": "error"}
                    ), 400
            except Exception as e:
                return jsonify(
                    message=str(e),
                    printout=output_str,
                    flash={"message": f"An unexpected error occurred: {e}", "category": "error"}
                ), 500
        else:
            # Handling for different types of errors
            if result_dict['error']:
                return jsonify(
                    message=result_dict['error'],
                    printout=output_str,
                    flash={"message": result_dict['error'], "category": "error"}
                ), 400
            elif result_dict['timeout']:
                return jsonify(
                    message="Timeout Occurred!",
                    printout=output_str,
                    flash={"message": "A timeout occurred during the execution of your submission.", "category": "warning"}
                ), 408
            elif result_dict['exception']:
                return jsonify(
                    message=result_dict['exception'],
                    printout=output_str,
                    flash={"message": result_dict['exception'], "category": "error"}
                ), 500

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
        #Get the challenge details
        challenge = SqlService.get_challenge_by_id(challenge_id)

        #Get the challenge test cases
        testcases = SqlService.get_challenge_tests_by_id(challenge_id)
        comments = SqlService.get_challenge_comments_by_id(challenge_id)
        if 'user_id' in session:
            account_id = session['user_id']
            submission = SqlService.get_challenge_submissions_by_id_and_account_id(challenge_id, account_id)
        else:
            submission = None

        if challenge:
            return render_template('challenge.html', challenge=challenge, testcases=testcases, comments = comments, submission = submission)
        else: 
            return abort(404)

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
        if session['user_id']:
            try:
                comment_title = request.form['comment-title']
                comment_content = request.form['comment-content']

                #If the user enters an empty title or comment 
                if(comment_title == None or comment_content == None):
                    return redirect(url_for('generic_challenge', challenge_id=challenge_id))
                
                #Inserting the comment to the challenge
                else:
                    insert_id = SqlService.insert_challenge_comment(session['user_id'],challenge_id, comment_title, comment_content)

            except RuntimeError as err:
                print(f"Error! {err}")
                

        return redirect(url_for('generic_challenge', challenge_id=challenge_id))

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
        try:
            if session['privileged_mode']:
                delete_confirmation = SqlService.delete_challenge_by_id(challenge_id)

            #delete_test_confirmation = SqlService.get_challenge_test_by_id(challenge_id)
          
        except RuntimeError as err:
            print(f"Error! {err}")
        return redirect(url_for('challenges'))

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
        #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            #return_value = SqlService.update_challenge_name_by_id(challenge_id)
            new_challenge_name = request.json

            if session['privileged_mode']:
                SqlService.update_challenge_name_by_id(challenge_id, new_challenge_name['new_challenge_name'])
                return jsonify({'message': 'ok'}), 200
        except RuntimeError as err:
            print(f"Error occurred while updating challenge name! {err}")
        
        return redirect(url_for('generic_challenge', challenge_id=challenge_id))


        

    def edit_challenge_difficulty(self, challenge_id):
         """
        Updates the difficulty level of a challenge if the user has the appropriate privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge to be edited.

        Returns:
            A JSON response indicating whether the update was successful, with an HTTP status code
            of 200 for success or 403 for permission denied. Flash messages provide user feedback.
        """
         try:
            new_difficulty_level = request.json

            if session['privileged_mode']:
                SqlService.update_challenge_difficulty_by_id(challenge_id,new_difficulty_level['newValue'])
                return jsonify({'message': 'ok'}), 200
         except:
             return jsonify({'message': 'unautorized user'}), 403
        
             
         
       

    def edit_challenge_description(self, challenge_id):
        """
        Edits the description of a challenge, given that the user has the necessary privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge to be edited.

        Returns:
            A JSON response indicating the outcome of the update with an HTTP status code of 200
            for success or 403 for permission denied. Flash messages provide feedback to the user.
        """
        #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            #return_value = SqlService.update_challenge_name_by_id(challenge_id)
            new_challenge_discr = request.json

            if session['privileged_mode']:
                SqlService.update_challenge_description_by_id(challenge_id, new_challenge_discr['new_challenge_discr'])
                return jsonify({'message': 'ok'}), 200
        
        except RuntimeError as err:
            print(f"Error occurred while updating challenge name! {err}")
        
        return redirect(url_for('generic_challenge', challenge_id=challenge_id))


    def edit_challenge_stub_name(self, challenge_id):
        """
        Updates the stub name of a challenge if the user has privileged access.

        Parameters:
            challenge_id (int): The unique identifier for the challenge whose stub name is to be updated.

        Returns:
            A JSON response indicating the success status of the update, with an HTTP status code of 200
            for success or 403 for permission denied. Flash messages provide feedback on the action's outcome.
        """
         #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            #return_value = SqlService.update_challenge_name_by_id(challenge_id)
            new_stub_name = request.json

            if session['privileged_mode']:
                SqlService.update_challenge_stub_name_by_id(challenge_id, new_stub_name['stub_name'])
                return jsonify({'message': 'ok'}), 200
        
        except RuntimeError as err:
            print(f"Error occurred while updating challenge name! {err}")
        
        return redirect(url_for('generic_challenge', challenge_id=challenge_id))


    def edit_challenge_stub_block(self, challenge_id):
        """
        Edits the code stub (skeleton code) for a challenge if the user has administrative privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge whose stub is to be updated.

        Returns:
            A JSON response indicating success or failure of the update, with corresponding flash messages
            and an HTTP status code of 200 for success or 403 for permission denied.
        """
        #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            new_stub_block = request.form['stub-block']
            if session['privileged_mode']:
                SqlService.update_challenge_stub_block_by_id(challenge_id, new_stub_block)
                #returning an Okay message to the caller
                return  redirect(url_for('generic_challenge', challenge_id=challenge_id))
           

        except RuntimeError as err:
            print(f"Error occurred adding new test case. {err}")
        
        return  redirect(url_for('generic_challenge', challenge_id=challenge_id))

    def add_test_case(self, challenge_id):
        """
        Adds a new test case to a challenge if the user has the required privileges.

        Parameters:
            challenge_id (int): The unique identifier for the challenge to which the test case will be added.

        Returns:
            A JSON response indicating whether the test case was successfully added, with an HTTP status code
            of 200 for success or 403 for permission denied. Flash messages provide user feedback.
        """
        #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            input_parameter = request.form['inputParameters[]']
            output_parameter = request.form['expectedOutput[]']

            if session['privileged_mode']:
                SqlService.insert_challenge_test(challenge_id, input_parameter, output_parameter)
           
        except RuntimeError as err:
            print(f"Error occurred adding new test case. {err}")
        
        return  redirect(url_for('generic_challenge', challenge_id=challenge_id))
        

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
        #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            if session['privileged_mode']:
                SqlService.delete_challenge_test_by_id_and_challenge_id(test_case_id, challenge_id)
                return jsonify({'message': 'ok'}), 200

        except RuntimeError as err:
            print(f"Error has occurred while deleting a test case. {err}")

        redirect(url_for('generic_challenge', challenge_id=challenge_id))
        
        

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

        #agin here I do not have a session variable set yet to check the user privileged acess
        #It will be included once the session variable is created

        try:
            if session['privileged_mode']:
                SqlService.delete_challenge_comment_by_id_and_challenge_id(comment_id, challenge_id)
            
        except RuntimeError as err:
            print(f'Error Deleting Comment! {err}')
        return  redirect(url_for('generic_challenge', challenge_id=challenge_id))

        
    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == '__main__':
    my_app = App()
    
    my_app.run(debug=True)
    