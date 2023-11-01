import sys

sys.path.append("..")
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db, fetch_hashed_password, \
    get_validation_code, alter_validation_state, is_account_verified
from verifymail import send_email, verification_code, VerifyCodeForm
from flask import render_template, flash, url_for, redirect

sender = "huangzhe406@gmail.com"
emailpassword = "mguvsoybbnterbkj"

'''
Allows a user to login to their verified account
:param email: the user's email associated with their account
:param password: the user's chosen password for their account
:param err: error code if needed
:return: access to the page if they succeed, same page otherwise
'''
def login(email, password, err):
    hashed_password_from_db = fetch_hashed_password(email)
    if hashed_password_from_db is not None:
        flag = is_account_verified(email)
        if flag[0] == 0:
            login_errors = {"loginemail": ["Email address has not been veirfied!", ]}
            login_errors.update(err)
            return render_template('index.html', errors=login_errors)
        if verify_password(password, hashed_password_from_db):
            return redirect(url_for('landing_page'))
        else:
            login_errors = {"loginpassword": ["Password error!"]}
            login_errors.update(err)
            return render_template('index.html', errors=login_errors)
    else:
        login_errors = {"loginemail": ["Email address has not been used to register, please register first!"]}
        login_errors.update(err)
        return render_template('index.html', errors=login_errors)


'''
Allows a user to register their account
:param first_name: the first name of a user
:param last_name: the last name of a user
:param email: the email of a user
:param password: the chosen password for a user
:param err: error code if needed
:return: if they successfully registered or not
'''
def register(first_name, last_name, email, password, err):
    hashed_password = hash_password(password)
    ver_code = verification_code()
    try:
        result = insert_user_into_db(first_name, last_name, email, hashed_password, ver_code)
        if result:
            if send_email(subject='Verified Code', body=ver_code, sender=sender, recipients=[email, ],
                          password=emailpassword):
                return redirect(url_for('verify'))
            else:
                flash("Registration failed, database is busy now")
                return render_template('index.html', errors=err)
        else:
            login_errors = {"email": ["This email address is used, try another email address!"]}
            return render_template('index.html', errors=login_errors)
    except Exception as e:
        print(f"Error during registration: {str(e)}")


'''
Verify the users account
:param user_ver_code: the unique verification code for a user
:param user_email: the email of the user
:return: access to the site if they succeed, stay on page if they fail
'''
def verification(user_ver_code, user_email):
    db_ver_code = get_validation_code(user_email)[0]
    if user_ver_code == db_ver_code:
        alter_validation_state(email=user_email)
        return redirect(url_for('landing_page'))
    else:
        flash("Verified code is incorrect!")
        return redirect(url_for('verify'))
