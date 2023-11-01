import mysql.connector


'''
Connects to our database
'''
def connect_to_database():
    connection = mysql.connector.connect(
        # mysql.connector is python3, pysql was from python2. use pip3 install mysql-connector-python
        host='flask-app-rds-cluster.chnoobsehdtd.us-east-1.rds.amazonaws.com',
        user='tvbum_admin',
        password='od9KN7pOhEV32oz',
        database='flask_app_db'
    )
    return connection


'''
Executes the query on the database
:param connection: connection to the database
:param query: the query for the database
:param params: the params in the query if needed, default None
:return: true if they match, false if they don't
'''
def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()


'''
Inserts a user into our database
:param first_name: the first name of a user
:param last_name: the last name of a user
:param email: the email of a user
:param hashed_password: the hashed password of a user
:param first_name: validation code of a user
:return: true if they were added to the db properly, false if they were not
'''
def insert_user_into_db(first_name, last_name, email, hashed_password, validation_code):
    try:
        # Connect to the database
        connection = connect_to_database()
        insert_query = "INSERT INTO users (first_name, last_name, email, hashed_password, validationcode, isvalidation) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (first_name, last_name, email, hashed_password, validation_code, 0)
        # Execute the SQL query to insert the user data
        execute_query(connection, insert_query, data)
        connection.commit()
        connection.close()
        return True

    except Exception as e:
        # Handle any exceptions 
        print(f"Error inserting user data into the database: {str(e)}")
        return False


'''
Fetches the hashed password of user
:param email: the email of a user
:return: the hashed password if the user exists, None otherwise
'''
def fetch_hashed_password(email):
    try:
        # Connect to the database
        connection = connect_to_database()

        # Define the SQL query to fetch the hashed password based on email
        select_query = "SELECT hashed_password FROM users WHERE email = %s"
        data = (email,)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(select_query, data)

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            return result['hashed_password']
        else:
            return None

    except Exception as e:
        # Handle any exceptions or errors that may occur during database retrieval
        print(f"Error fetching hashed password from the database: {str(e)}")
        return None


'''
Checks that a user properly verified their account
:param email: the email of a user
:param hashed_password: the hashed password of a user
:param first_name: validation code of a user
:return: true if they were verified properly, false if they were not
'''
def is_account_verified(email):
    try:
        connection = connect_to_database()

        select_query = "select isvalidation from users where email = %s"
        data = (email,)

        cursor = connection.cursor()
        cursor.execute(select_query, data)

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error fetching isvalidion from db: {str(e)}")
        return None


'''
Gets the validation code for a user
:param email: the email of a user
:return: true if the validation code was found, None otherwise
'''
def get_validation_code(email):
    try:
        connection = connect_to_database()

        select_query = "select validationcode from users where email = %s"
        data = (email,)

        cursor = connection.cursor()
        cursor.execute(select_query, data)

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error getting validation code from db: {str(e)}")
        return None


'''
Alters if a user was verified or not
:param email: the email of a user
'''
def alter_validation_state(email):
    try:
        connection = connect_to_database()

        updata_query = "UPDATE users SET isvalidation=true WHERE email = %s"
        data = (email,)

        cursor = connection.cursor()
        cursor.execute(updata_query, data)

        cursor.close()
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error altering validation code in db: {str(e)}")
        return None


'''
Gets the information about a user just from their email
:param email: the email of a user
:return: the result of the query if they were found, None if they were not
'''
def get_user_details_by_email(email):
    try:
        connection = connect_to_database()
        select_query = "SELECT first_name, last_name, user_id FROM users WHERE email = %s"
        data = (email,)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(select_query, data)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return result
        else:
            print("User not found in the database.")
            return None
    except Exception as e:
        print(f"Error fetching user details from the database: {str(e)}")
        return None


'''
Adds a show to the user's watch list
:param user_id: id of the user adding to their watch list
:param mov_show_id: id of the movie or show
:param media_type: movie or tv show
:return: a message if it's already in the list, or success or fail
'''
def add_from_watchlist(user_id, mov_show_id, media_type):
    try:
        connection = connect_to_database()

        select_query = "SELECT * FROM watch_list WHERE user_id = %s AND mov_show_id = %s"
        data = (user_id, mov_show_id)

        cursor = connection.cursor()
        cursor.execute(select_query, data)
        existing_entry = cursor.fetchone()

        if existing_entry:
            message = "Movie/Show is already in the watchlist."
            print(str(message))
            return message
        insert_query = "INSERT INTO watch_list (user_id, mov_show_id, media_type) VALUES (%s, %s, %s)"
        data = (user_id, mov_show_id, media_type)
        execute_query(connection, insert_query, data)

        connection.commit()
        connection.close()
        message = "Movie/Show added to watchlist successfully."
        print(str(message))
        return message

    except Exception as e:
        # Handle any exceptions or errors that may occur during database insertion
        print(f"Error adding to watchlist: {str(e)}")
        return "An error occurred while adding to watchlist."


'''
Removes a show or movie from someone's watch lsit
:param user_id: id of the user adding to their watch list
:param mov_show_id: id of the movie or show
:return: a message if the show was successfully added or removed
'''
def remove_from_watchlist(user_id, mov_show_id):
    try:
        connection = connect_to_database()

        delete_query = "DELETE FROM watch_list WHERE user_id = %s AND mov_show_id = %s"
        data = (user_id, mov_show_id)

        execute_query(connection, delete_query, data)

        connection.commit()
        connection.close()
        message = "Movie/Show removed from watchlist successfully."
        print(str(message))
        return True

    except Exception as e:
        # Handle any exceptions or errors that may occur during database deletion
        print(f"Error removing from watchlist: {str(e)}")
        return False


'''
Gets a user's full watch list
:param user_id: id of the user adding to their watch list
:return: the movies/ shows on the watch list
'''
def get_watchlist_movies(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        select_query = "SELECT mov_show_id, media_type FROM watch_list WHERE user_id = %s"
        select_data = (user_id,)
        cursor.execute(select_query, select_data)

        watchlist_movies = cursor.fetchall()

        connection.close()
        return watchlist_movies

    except Exception as e:
        # Handle any exceptions or errors that may occur during database selection
        print(f"Error fetching watchlist movies: {str(e)}")
        return []
