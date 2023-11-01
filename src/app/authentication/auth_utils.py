import bcrypt


'''
Hashes the password for secure storage
:param plain_text_password: the plain text password for a user
:return: the password that's been salted and hashed
'''
def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password


'''
Verifies the password enters matched the one stored
:param password: the password a user enters to login
:param hashed_password_from_db: the stored hashed password in the database
:return: true if they match, false if they don't
'''
def verify_password(password, hashed_password_from_db):
    password = password.encode('utf-8')  # Ensure password is bytes
    hashed_password_from_db = hashed_password_from_db.encode('utf-8')  # Ensure hashed_password_from_db is bytes
    return bcrypt.checkpw(password, hashed_password_from_db)




