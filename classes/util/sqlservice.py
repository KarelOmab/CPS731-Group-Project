from dotenv import load_dotenv
import os
import mysql.connector
from classes.account.user import User
from classes.account.moderator import Moderator
from classes.challenge.challenge import Challenge
from classes.challenge.challengetest import ChallengeTest
from classes.challenge.challengecomment import ChallengeComment
from classes.challenge.challengesubmission import ChallengeSubmission

# Load environment variables from .env file
load_dotenv()

class SqlService:
    # Database configuration as class variables
    HOST = os.getenv("MYSQL_HOST", "localhost")
    USER = os.getenv("MYSQL_USER", "root")
    PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    DATABASE = os.getenv("MYSQL_DB", "CodeChamp-mockup")

    @staticmethod
    def create_connection():
        """
        Establishes a connection to the SQL database using predefined configuration.

        This method utilizes the MySQL Connector/Python to create a connection to the database.
        It uses configuration details such as host, user, password, and database name which are
        set as class attributes.

        Returns:
            mysql.connector.connection.MySQLConnection: An instance of the connection object to the database.
        """
        config = {
            "host": SqlService.HOST,
            "user": SqlService.USER,
            "password": SqlService.PASSWORD,
            "database": SqlService.DATABASE
        }
        return mysql.connector.connect(**config)

    @staticmethod
    def execute_query(query, params=None):
        """
        Executes a given SQL query and returns the fetched results.

        This method creates a database connection, executes the provided SQL query, and fetches
        all the resulting rows. It supports parameterized queries to prevent SQL injection. In case
        of an error, it prints the error message and returns None.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be used in a parameterized query.

        Returns:
            list of dict or None: A list of dictionaries representing the fetched rows if the query
                                is successful, or None if there is an error.
        """
        connection = SqlService.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def execute_query_and_get_last_id(query, params):
        """
        Executes a given SQL query and returns the ID of the last inserted row.

        This method is intended for use with queries that insert a row into the database. It commits
        the transaction and returns the ID of the newly inserted row. If the query fails, it rolls back
        the transaction and returns None.

        Args:
            query (str): The SQL query to be executed.
            params (tuple): The parameters to be used in a parameterized query.

        Returns:
            int or None: The ID of the last row inserted by the query if successful, or None if there is an error.
        """
        connection = SqlService.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def call_stored_procedure(proc_name, params=(), fetchone=False, update=False, delete=False):
        """
        Calls a stored procedure in the SQL database with the provided parameters.

        This method can be used to execute a stored procedure for fetching results, updating, or deleting
        records. It allows for fetching either a single result or all results based on the 'fetchone'
        parameter. The 'update' and 'delete' flags indicate if the stored procedure is expected to update
        or delete records, respectively.

        Args:
            proc_name (str): The name of the stored procedure to call.
            params (tuple, optional): The parameters to pass to the stored procedure.
            fetchone (bool, optional): If True, fetches a single result from the called procedure.
            update (bool, optional): If True, indicates that the procedure is expected to perform an update.
            delete (bool, optional): If True, indicates that the procedure is expected to perform a delete operation.

        Returns:
            list, dict, bool, or None: Depending on the flags set and the procedure called, it may return:
                                    - A list of dictionaries representing the fetched rows.
                                    - A single dictionary if 'fetchone' is True.
                                    - True if an 'update' or 'delete' was performed.
                                    - None if there is an error.
        """
        connection = SqlService.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.callproc(proc_name, params)
            connection.commit()
            if fetchone:
                for result in cursor.stored_results():
                    return result.fetchone()
            elif update or delete:
                return True
            else:
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                return results
        except mysql.connector.Error as err:
            #print(f"Error: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def raw_account_to_account(raw_account):
        """
        Transforms a raw account data dictionary into an appropriate User or Moderator object.

        Based on the usergroup ID within the raw account data, this method decides whether to instantiate a User or Moderator object. It checks against predefined usergroup IDs to determine the type of user. If the usergroup ID matches that of a Moderator, a Moderator object is returned. If it matches that of a regular User, a User object is returned. If the usergroup ID does not match any known user types, the method returns None.

        Parameters:
        - raw_account (dict): A dictionary containing the keys and values for an account's attributes.

        Returns:
        - User or Moderator: An instantiated object of type User or Moderator based on the usergroup ID in the raw_account data.
        - None: If the usergroup_id does not correspond to a recognized type of user.

        Constants:
        - USERGROUP_MOD=2 (int): The usergroup ID representing a Moderator.
        - USERGROUP_USER=3 (int): The usergroup ID representing a regular User.

        Example of a raw_account dictionary:
        {
            'id': 123,
            'created_at': '2021-01-01T00:00:00Z',
            'usergroup_id': 2,
            'username': 'moderatorUser',
            'email': 'mod@example.com'
        }

        Notes:
        - The usergroup IDs are hardcoded within the method. USERGROUP_MOD corresponds to moderators, and USERGROUP_USER corresponds to regular users.
        """
        if not raw_account:
            return None
        
        account_id = raw_account['id']
        created_at = raw_account['created_at']
        usergroup_id = raw_account['usergroup_id']
        username = raw_account['username']
        email = raw_account['email']

        USERGROUP_MOD = 2
        USERGROUP_USER = 3

        if usergroup_id == USERGROUP_MOD:
            return Moderator(account_id, username)
        elif usergroup_id == USERGROUP_USER:
            return User(account_id, username)

        return None
    
    @staticmethod
    def raw_challenge_to_challenge(raw_challenge):
        """
        Converts a raw challenge dictionary to a Challenge object.

        This method takes a dictionary containing challenge data, typically retrieved from a database, and converts it into a Challenge object by extracting the individual pieces of data and passing them to the Challenge constructor.

        Parameters:
        - raw_challenge (dict): A dictionary containing the keys and values for challenge attributes.

        Returns:
        - Challenge: An instantiated Challenge object with properties populated from the raw_challenge dictionary.

        Example of a raw_challenge dictionary:
        {
            'id': 1,
            'created_at': '2021-01-01T00:00:00Z',
            'account_id': 10,
            'is_deleted': False,
            'name': 'Sample Challenge',
            'difficulty': 'Easy',
            'description': 'This is a sample challenge.',
            'stub_name': 'sample_challenge',
            'stub_block': 'def sample_challenge():',
            'time_allowed_sec': 60
        }
        """
        if not raw_challenge:
            return None
        
        challenge_id = raw_challenge['id']
        created_at = raw_challenge['created_at']
        account_id = raw_challenge['account_id']
        is_deleted = raw_challenge['is_deleted']
        name = raw_challenge['name']
        difficulty = raw_challenge['difficulty']
        description = raw_challenge['description']
        stub_name = raw_challenge['stub_name']
        stub_block = raw_challenge['stub_block']
        time_allowed_sec = raw_challenge['time_allowed_sec']
        challenge = Challenge(challenge_id, created_at, account_id, is_deleted, name, difficulty, description, stub_name, stub_block, time_allowed_sec)
        return challenge
    
    @staticmethod
    def raw_test_to_test(raw_test):
        """
        Transforms a raw test data dictionary into a ChallengeTest object.

        It extracts data from the dictionary, such as the test's unique identifier, associated challenge ID, input, and expected output, and initializes a ChallengeTest object with these attributes.

        Parameters:
        - raw_test (dict): The dictionary containing test attributes.

        Returns:
        - ChallengeTest: A new ChallengeTest object instantiated with the data from raw_test.

        Example of a raw_test dictionary:
        {
            'id': 100,
            'challenge_id': 1,
            'is_deleted': False,
            'input': 'Test input',
            'output': 'Expected output'
        }
        """
        test_id = raw_test['id']
        challenge_id = raw_test['challenge_id']
        is_deleted = raw_test['is_deleted']
        test_input = raw_test['input']
        test_output = raw_test['output']
        test = ChallengeTest(test_id, challenge_id, is_deleted, test_input, test_output)
        return test
    
    @staticmethod
    def raw_comment_to_comment(raw_comment):
        """
        Creates a ChallengeComment object from a raw comment dictionary.

        This method parses a dictionary containing details of a comment, like its ID, associated account ID, challenge ID, and content, and uses them to construct a ChallengeComment object.

        Parameters:
        - raw_comment (dict): A dictionary with keys corresponding to comment attributes.

        Returns:
        - ChallengeComment: The constructed ChallengeComment object containing the information from the raw_comment.

        Example of a raw_comment dictionary:
        {
            'id': 50,
            'created_at': '2021-01-01T00:00:00Z',
            'account_id': 10,
            'is_deleted': False,
            'challenge_id': 1,
            'title': 'Interesting Challenge',
            'text': 'This was a thought-provoking challenge.',
            'username': 'johndoe'
        }
        """
        comment_id = raw_comment['id']
        created_at = raw_comment['created_at']
        account_id = raw_comment['account_id']
        is_deleted = raw_comment['is_deleted']
        challenge_id = raw_comment['challenge_id']
        title = raw_comment['title']
        text = raw_comment['text']
        username = raw_comment['username']
        comment = ChallengeComment(comment_id, created_at, account_id, is_deleted, challenge_id, title, text, username)
        return comment
    
    @staticmethod
    def raw_submission_to_submission(raw_submission):
        """
        Converts raw submission data into a ChallengeSubmission object.

        The function extracts information from a dictionary, such as the submission ID, the time taken to execute, the number of characters in the code, the source code, and other relevant data, and uses it to instantiate a ChallengeSubmission object.

        Parameters:
        - raw_submission (dict): Dictionary containing the submission details.

        Returns:
        - ChallengeSubmission: An object representing the submission with attributes populated from the raw_submission.

        Example of a raw_submission dictionary:
        {
            'id': 200,
            'created_at': '2021-02-01T12:00:00Z',
            'challenge_id': 1,
            'account_id': 10,
            'exec_time': 1.2,
            'exec_chars': 150,
            'exec_src': 'print("Hello World")'
        }
        """
        submission_id = raw_submission['id']
        created_at = raw_submission['created_at']
        challenge_id = raw_submission['challenge_id']
        account_id = raw_submission['account_id']
        exec_time = raw_submission['exec_time']
        exec_chars = raw_submission['exec_chars']
        exec_src = raw_submission['exec_src']
        submission = ChallengeSubmission(submission_id, created_at, challenge_id, account_id, exec_time, exec_chars, exec_src)
        return submission

    @staticmethod
    def insert_account(usergroup, username, password, email):
        """
        Inserts a new account into the database via a stored procedure.

        This method calls the 'InsertAccount' stored procedure, which is expected to insert
        a new account record into the database with the provided user details.

        Args:
            usergroup (str): The group or role associated with the user.
            username (str): The username for the account.
            password (str): The password for the account.
            email (str): The email address for the account.

        Returns:
            'Success' message, 'Username in use' message or 'Email in use' message
        """
        return SqlService.call_stored_procedure("InsertAccount", params=(usergroup, username, password, email))

    @staticmethod
    def insert_challenge(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec):
        """
        Inserts a new coding challenge into the database via a stored procedure.

        Calls the 'InsertChallenge' stored procedure to insert a new challenge record
        associated with the provided account ID. Additional challenge details such as
        difficulty and allowed time are also passed as arguments.

        Args:
            account_id (int): The ID of the account creating the challenge.
            name (str): The name of the challenge.
            difficulty (str): The difficulty level of the challenge.
            description (str): A description of the challenge.
            stub_name (str): The function name to be used as a stub for the challenge.
            stub_block (str): The code block to be used as a stub for the challenge.
            time_allowed_sec (int): The time in seconds allowed to solve the challenge.

        Returns:
            The result of the stored procedure execution, the ID of the
            inserted challenge if successful.
        """
        return SqlService.call_stored_procedure("InsertChallenge", params=(account_id, name, difficulty, description, stub_name, stub_block, time_allowed_sec))

    @staticmethod
    def insert_challenge_test(challenge_id, input_data, output_data):
        """
        Inserts a test case for a specific coding challenge into the database.

        This method utilizes the 'InsertChallengeTest' stored procedure to add a new
        test case with input and expected output to the specified challenge.

        Args:
            challenge_id (int): The ID of the challenge for which the test is added.
            input_data (str): The input data for the test case.
            output_data (str): The expected output data for the test case.

        Returns:
            The result of the stored procedure execution, the ID of the
            inserted challenge test if successful.
        """
        return SqlService.call_stored_procedure("InsertChallengeTest", params=(challenge_id, input_data, output_data))

    @staticmethod
    def insert_challenge_comment(account_id, challenge_id, title, text):
        """
        Inserts a comment on a challenge into the database via a stored procedure.

        Calls the 'InsertChallengeComment' stored procedure to add a comment made by a user
        (represented by the account ID) on a specific challenge.

        Args:
            account_id (int): The ID of the user's account making the comment.
            challenge_id (int): The ID of the challenge being commented on.
            title (str): The title of the comment.
            text (str): The text content of the comment.

        Returns:
            The result of the stored procedure execution, the ID of the
            inserted challenge comment if successful.
        """
        return SqlService.call_stored_procedure("InsertChallengeComment", params=(account_id, challenge_id, title, text))

    @staticmethod
    def insert_challenge_submission(challenge_id, account_id, exec_time, exec_chars, exec_src):
        """
        Inserts a challenge submission record into the database.

        This method invokes the 'InsertChallengeSubmission' stored procedure to record
        a user's attempt at solving a challenge. It includes execution details such as
        time taken and characters used.

        Args:
            challenge_id (int): The ID of the challenge that was attempted.
            account_id (int): The ID of the user's account that submitted the attempt.
            exec_time (float): The execution time of the attempt in seconds.
            exec_chars (int): The number of characters in the submission source code.
            exec_src (str): The actual source code of the submission.

        Returns:
            The result of the stored procedure execution, the ID of the submission
            if successful.
        """
        return SqlService.call_stored_procedure("InsertChallengeSubmission", params=(challenge_id, account_id, exec_time, exec_chars, exec_src))

    @staticmethod
    def get_account_by_username_password(username, password):
        """
        Retrieves an account from the database based on the provided username and password.

        This method calls the 'GetAccountByUsernameAndPassword' stored procedure and expects
        to fetch a single account that matches the provided credentials. It then converts the
        raw account data into a more structured account object.

        Args:
            username (str): The username of the account to retrieve.
            password (str): The password associated with the account.

        Returns:
            A structured account object if the retrieval is successful, or None if no matching
            account is found or if an error occurs.
        """
        raw_account = SqlService.call_stored_procedure("GetAccountByUsernameAndPassword", params=(username, password), fetchone=True)
        account = SqlService.raw_account_to_account(raw_account)
        return account
    
    @staticmethod
    def get_all_challenges():
        """
        Retrieves a list of all challenges from the database.

        This method calls the 'GetAllChallenges' stored procedure which is expected to
        return all challenges in the database. Each raw challenge data is then converted
        into a structured challenge object.

        Returns:
            A list of challenge objects representing all challenges in the database.
        """
        raw_challenges = SqlService.call_stored_procedure("GetAllChallenges")
        challenges = []
        for raw_challenge in raw_challenges:
            challenge = SqlService.raw_challenge_to_challenge(raw_challenge)
            challenges.append(challenge)
        return challenges


    @staticmethod
    def get_challenge_by_id(id):
        """
        Retrieves a single challenge from the database by its ID.

        This method calls the 'GetChallengeById' stored procedure, passing the specific
        challenge ID to retrieve the corresponding challenge. The raw challenge data
        is converted into a structured challenge object.

        Args:
            id (int): The unique identifier for the challenge to retrieve.

        Returns:
            A challenge object corresponding to the specified ID or None if not found.
        """
        raw_challenge = SqlService.call_stored_procedure("GetChallengeById", params=(id, ), fetchone=True)
        challenge = SqlService.raw_challenge_to_challenge(raw_challenge)
        return challenge
    
    @staticmethod
    # get a specific challenge test
    def get_challenge_test_by_id(challenge_test_id):
        """
        Retrieves a specific test case for a given challenge test ID.

        Calls the 'GetChallengeTestById' stored procedure with the challenge test ID to fetch
        the associated test case. The test case data is transformed into a structured
        test object.

        Args:
            challenge_test_id (int): The unique identifier for the challenge test whose test cases is to be retrieved.

        Returns:
            A test object for the specified challenge.
        """
        raw_test = SqlService.call_stored_procedure("GetChallengeTestById", params=(challenge_test_id, ), fetchone=True)
        test = SqlService.raw_test_to_test(raw_test)
        return test

    @staticmethod
    # unlimited version
    def get_challenge_tests_by_id(id):
        """
        Retrieves all test cases for a given challenge by its ID without any limit.

        Calls the 'GetChallengeTestsById' stored procedure with the challenge ID to fetch
        all associated test cases. Each raw test case data is transformed into a structured
        test object.

        Args:
            id (int): The unique identifier for the challenge whose test cases are to be retrieved.

        Returns:
            A list of test objects for the specified challenge.
        """
        raw_tests = SqlService.call_stored_procedure("GetChallengeTestsById", params=(id, ))
        if not raw_tests:
            return None
        
        tests = []
        for raw_test in raw_tests:
            test = SqlService.raw_test_to_test(raw_test)
            tests.append(test)
        return tests

    @staticmethod
    def get_challenge_tests_by_id_and_limit(id):
        """
        Retrieves a limited number of test cases for a given challenge by its ID.

        This method uses the 'GetChallengeTestsByIdAndLimit' stored procedure with the
        challenge ID and a predefined limit to fetch a subset of test cases. Each raw test
        case data is converted into a structured test object.

        Args:
            id (int): The unique identifier for the challenge whose test cases are to be retrieved.

        Returns:
            A list of test objects, limited to a predefined number, for the specified challenge.
        """
        MY_LIMIT = 5
        raw_tests = SqlService.call_stored_procedure("GetChallengeTestsByIdAndLimit", params=(id, MY_LIMIT))
        tests = []
        for raw_test in raw_tests:
            test = SqlService.raw_test_to_test(raw_test)
            tests.append(test)
        return tests
    
    @staticmethod
    def get_challenge_comment_by_id(comment_id):
        """
        Retrieves all specific comment for a specific challenge by its ID.

        Invokes the 'GetChallengeCommentById' stored procedure to
        obtain a specific comment that is then turned into a structured comment object.

        Args:
            comment_id (int): The unique identifier for the challenge comment to be retrieved.

        Returns:
            A comment object for the specified challenge.
        """
        raw_comment = SqlService.call_stored_procedure("GetChallengeCommentById", params=(comment_id, ), fetchone=True)
        comment = SqlService.raw_comment_to_comment(raw_comment)
        return comment

    @staticmethod
    def get_challenge_comments_by_id(id):
        """
        Retrieves all comments for a specific challenge by its ID.

        Invokes the 'GetChallengeCommentsById' stored procedure with the challenge ID to
        obtain all comments made on that challenge. Each raw comment data is then turned
        into a structured comment object.

        Args:
            id (int): The unique identifier for the challenge whose comments are to be retrieved.

        Returns:
            A list of comment objects for the specified challenge.
        """
        raw_comments = SqlService.call_stored_procedure("GetChallengeCommentsById", params=(id, ))
        comments = []
        for raw_comment in raw_comments:
            comment = SqlService.raw_comment_to_comment(raw_comment)
            comments.append(comment)
        return comments
    
    @staticmethod
    def get_challenge_submission_by_id(submission_id):
        """
        Retrieves a specific submission for a challenge.

        This method calls the 'GetChallengeSubmissionById' stored procedure,
        passing the submission ID to fetch the specified submission.
        It then converts each raw submission data into a structured submission object.

        Args:
            challesubmission_idnge_id (int): The ID of the submission that is sought.

        Returns:
            A submission objects corresponding to the specified submission_id.
        """
        raw_submission = SqlService.call_stored_procedure("GetChallengeSubmissionById", params=(submission_id, ), fetchone=True)
        submission = SqlService.raw_submission_to_submission(raw_submission)
        return submission

    @staticmethod
    def get_challenge_submissions_by_id_and_account_id(challenge_id, account_id):
        """
        Retrieves all submissions for a specific challenge made by a specific account.

        This method calls the 'GetChallengeSubmissionsByIdAndAccountId' stored procedure,
        passing the challenge ID and account ID to fetch submissions relevant to both identifiers.
        It then converts each raw submission data into a structured submission object.

        Args:
            challenge_id (int): The ID of the challenge for which submissions are sought.
            account_id (int): The ID of the account whose submissions are sought.

        Returns:
            A list of submission objects corresponding to the specified challenge and account.
        """
        raw_submissions = SqlService.call_stored_procedure("GetChallengeSubmissionsByIdAndAccountId", params=(challenge_id, account_id))
        submissions = []
        for raw_submission in raw_submissions:
            submission = SqlService.raw_submission_to_submission(raw_submission)
            submissions.append(submission)
        return submissions

    @staticmethod
    def update_challenge_name_by_id(id, name):
        """
        Updates the name of a challenge based on its unique identifier.

        This method invokes a stored procedure to update the name of a challenge in the database. It uses the challenge's unique ID to locate the record and update its name to the provided value.

        Parameters:
        - id (int): The unique identifier of the challenge.
        - name (str): The new name to update the challenge with.

        Returns:
        - The result of the stored procedure execution which may contain information about the success or failure of the update operation.
        """
        return SqlService.call_stored_procedure("UpdateChallengeNameById", params=(id, name), update=True)

    @staticmethod
    def update_challenge_difficulty_by_id(id, difficulty):
        """
        Updates the difficulty level of a challenge based on its ID.

        Calls a stored procedure to change the difficulty of a specific challenge. The method requires the challenge's ID and the new difficulty level to be set.

        Parameters:
        - id (int): The unique identifier of the challenge to be updated.
        - difficulty (str): The new difficulty level to set for the challenge.

        Returns:
        - The outcome of the stored procedure, indicating the update status.
        """
        return SqlService.call_stored_procedure("UpdateChallengeDifficultyById", params=(id, difficulty), update=True)

    @staticmethod
    def update_challenge_description_by_id(id, description):
        """
        Updates the description of a challenge identified by its ID.

        This method calls a stored procedure in the database to update the description field
        of a specific challenge.

        Parameters:
        - id (int): The unique identifier of the challenge to be updated.
        - description (str): The new description text for the challenge.

        Returns:
        - The result of the stored procedure execution, typically a confirmation of the update.
        """
        return SqlService.call_stored_procedure("UpdateChallengeDescriptionById", params=(id, description), update=True)

    @staticmethod
    def update_challenge_stub_name_by_id(id, name):
        """
        Updates the stub name of a challenge based on the challenge's ID.

        Parameters:
        - id (int): The ID of the challenge to update.
        - name (str): The new stub name to be set for the challenge.

        Returns:
        - The result of the stored procedure execution, which is an indicator of success or failure.
        """
        return SqlService.call_stored_procedure("UpdateChallengeStubNameById", params=(id, name), update=True)

    @staticmethod
    def update_challenge_stub_block_by_id(id, stub_block):
        """
        Updates the stub block of code for a challenge identified by its ID.

        Parameters:
        - id (int): The ID of the challenge whose stub block is to be updated.
        - stub_block (str): The new code block that will replace the existing stub.

        Returns:
        - A confirmation of the update from the stored procedure's result.
        """
        return SqlService.call_stored_procedure("UpdateChallengeStubBlockById", params=(id, stub_block), update=True)

    @staticmethod
    def delete_challenge_by_id(id):
        """
        Deletes a challenge from the system using its unique identifier.

        This method calls the corresponding stored procedure to remove a challenge from the database.

        Parameters:
        - id (int): The ID of the challenge to be deleted.

        Returns:
        - An indicator from the database operation about the success or failure of the deletion.
        """
        return SqlService.call_stored_procedure("DeleteChallengeById", params=(id, ), delete=True)

    @staticmethod
    def delete_challenge_test_by_id_and_challenge_id(challenge_test_id, challenge_id):
        """
        Deletes a test case associated with a challenge by using both their IDs.

        Parameters:
        - challenge_test_id (int): The ID of the test case to be deleted.
        - challenge_id (int): The ID of the challenge associated with the test case.

        Returns:
        - An outcome from the database procedure that may confirm deletion or report an error.
        """
        return SqlService.call_stored_procedure("DeleteChallengeTestByIdAndChallengeId", params=(challenge_test_id, challenge_id), delete=True)

    @staticmethod
    def delete_challenge_comment_by_id_and_challenge_id(comment_id, challenge_id):
        """
        Removes a comment from a challenge based on the comment's and challenge's IDs.

        Parameters:
        - comment_id (int): The ID of the comment to be deleted.
        - challenge_id (int): The ID of the challenge from which the comment will be deleted.

        Returns:
        - The result of the stored procedure which may be a success or error message.
        """
        return SqlService.call_stored_procedure("DeleteChallengeCommentByIdAndChallengeId", params=(comment_id, challenge_id), delete=True)
    
    @staticmethod
    def purge_account_by_username(username):
        """
        Wipes an account record from the database - used for unit test cleanup purposes.

        Parameters:
        - username (str): The username of the account to be wiped.
        """
        return SqlService.call_stored_procedure("PurgeAccountByUsername", params=(username,), delete=True)
    
    @staticmethod
    def purge_challenge_by_id(challenge_id):
        """
        Wipes a challenge record from the database - used for unit test cleanup purposes.

        Parameters:
        - challenge_id (id): The id of the challenge to be wiped.
        """
        return SqlService.call_stored_procedure("PurgeChallengeById", params=(challenge_id,), delete=True)
    
    @staticmethod
    def purge_challenge_test_by_id(challenge_test_id):
        """
        Wipes a challenge test record from the database - used for unit test cleanup purposes.

        Parameters:
        - challenge_test_id (id): The id of the challenge test to be wiped.
        """
        return SqlService.call_stored_procedure("PurgeChallengeTestById", params=(challenge_test_id,), delete=True)
    
    @staticmethod
    def purge_challenge_comment_by_id(challenge_comment_id):
        """
        Wipes a challenge comment record from the database - used for unit test cleanup purposes.

        Parameters:
        - challenge_comment_id (id): The id of the challenge comment to be wiped.
        """
        return SqlService.call_stored_procedure("PurgeChallengeCommentById", params=(challenge_comment_id,), delete=True)
    
    @staticmethod
    def purge_challenge_submission_by_id(challenge_submission_id):
        """
        Wipes a challenge submission record from the database - used for unit test cleanup purposes.

        Parameters:
        - challenge_submission_id (id): The id of the challenge submission to be wiped.
        """
        return SqlService.call_stored_procedure("PurgeChallengeSubmissionById", params=(challenge_submission_id,), delete=True)

