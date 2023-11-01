import sys
import pytest
sys.path.append("..")
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password,getValidationCode,alterValidationState,isAccountVerified
from verifymail import send_email,verification_code,VerifyCodeForm
from flask import Flask, render_template, request, flash, url_for, redirect


print("test login")

@pytest.mark.parametrize("email,password,key,result",[('1231','231233','loginemail','Email address has not been used to register, please registor first!'),
                                                      ('tstorm1538@gmail.com','qweqwqeqwe','loginemail',"Email address has not been veirfied!"),
                                                      ("wsuncle@bu.edu",'123123ddd3','loginpassword','Password error!')])
def test_login(email,password,key,result):
    err={}
    errorInfo=login(email,password,err)
    assert errorInfo[key][0]==result

print("test verification")
@pytest.mark.parametrize("userVerCode,userEmail,result",[('werweqer','tstorm1538@gmail.com',False),
                                                         ('I812Gq','tmmc12@bu.edu',True)])
def test_verification(userVerCode,userEmail,result):
    err={}
    Info=verification(userVerCode,userEmail,err)
    assert Info==result







##########################################################################################################
def login(email,password,err):
    hashed_password_from_db = fetch_hashed_password(email)
    if hashed_password_from_db != None:
        flag=isAccountVerified(email)
        if flag[0]==0:
            login_errors={"loginemail":["Email address has not been veirfied!",]}
            login_errors.update(err)
            # flash("Email address has not been veirfied !")
            return login_errors
        if verify_password(password, hashed_password_from_db):
            return login_errors
        else:
            login_errors={"loginpassword":["Password error!"]}
            login_errors.update(err)
            # flash("Password error!")
            return login_errors
    else:
        login_errors={"loginemail":["Email address has not been used to register, please registor first!"]}
        login_errors.update(err)
        # flash("Email address has not been used to register, please registor first!")
        return login_errors

def verification(userVerCode,userEmail,err):
    dbVerCode=getValidationCode(userEmail)[0]
    if userVerCode==dbVerCode:
        return True
    else:
        return False