from flask import Flask, render_template, request, session,redirect,url_for
from businessLogic.movieSearch import *
from validation import RegistrationForm
from verifymail import VerifyCodeForm
from authentication.appControl import login, register, verification
from database.db import *


app = Flask(__name__)
app.secret_key = "random string"
sender = "huangzhe406@gmail.com"
emailpassword = "mguvsoybbnterbkj"


'''
Main function for app
'''
@app.route('/')
def main():
    form = RegistrationForm(request.form)
    err = {"email": [], "password": [], "confirm_password": []}
    return render_template('index.html', form=form, errors=err)


'''
First page that is opened on the BUMTV site
You may register or login to an existing account
'''
@app.route('/home', methods=['GET', 'POST'])
def access_page():
    form = RegistrationForm(request.form)
    err = {"email": [], "password": [], "confirm_password": []}
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
        result= login(email=email, password=password, err=form.errors)
        if result:
            session['user_email'] = email
        return result
    elif request.form['submit'] == 'Register':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        if form.validate():
            return register(first_name=first_name, last_name=last_name, email=email, password=password, err=form.errors)
        else:
            return render_template('index.html', errors=form.errors)
    return render_template('index.html', form=form, errors=err)


'''
Verifies the code entered is the one that was sent prior to creating the account
'''
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form = VerifyCodeForm(request.form)
    if request.method == 'POST':
        userVerCode = request.form['verifycode']
        userEmail = request.form['email']
        return verification(userVerCode=userVerCode, userEmail=userEmail)
    return render_template('verify.html', errors=form.errors)


'''
Landing page once a user is logged into the app
'''
@app.route('/landing-page', methods=['GET', 'POST'])
def landing_page():
    try:
        if 'user_email' not in session:
            print('You must be logged in to do this action.')
            return redirect(url_for('main'))

        user_email = session['user_email']
        user_data = get_user_details_by_email(user_email)

        if not user_data:
            print('User not found in the database.')
            return redirect(url_for('main'))
        
        popular_movies, popular_tv_shows = get_popular()
        
        watchlist = get_watchlist_movies(user_data['user_id'])
        for item in watchlist:
            item['Title'] = get_name(item['mov_show_id'],item['media_type'])
        return render_template('landing_page.html',
                            user_first_name = user_data['first_name'],
                            popular_movies=popular_movies,
                            popular_tv_shows=popular_tv_shows, 
                            user_watchlist = watchlist)
    except Exception as e:
        print(str(e))
        return "An error occurred."

@app.route('/landing-page/modify_watchlist', methods=['POST'])
def modifyWatchlist():
    try:
        if 'user_email' not in session:
            print('You must be logged in to do this action.')
            return redirect(url_for('main'))

        user_email = session['user_email']
        user_data = get_user_details_by_email(user_email)

        if not user_data:
            print('User not found in the database.')
            return redirect(url_for('main'))

        user_id = user_data['user_id']
        mov_show_id = request.form.get('mov_show_id')
        media_type = request.form.get('media_type')
        action = request.form.get('action')
        if action == 'add':
            add_from_watchlist(user_id, mov_show_id,media_type)
        elif action == 'remove':
            remove_from_watchlist(user_id, mov_show_id)
        else:
            print('Invalid action specified.')
        return redirect(url_for('landing_page'))

    except Exception as e:
        print(str(e))
        return "An error occurred."

'''
Display search results for a user
'''
@app.route('/search')
def search_results():
    query = request.args.get('query')
    results = search_movies_and_tv_shows(query)
    return render_template('search_results.html', query=query, results=results)


'''
Profile page for a user
'''

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    try:
        if 'user_email' not in session:
            print('You must be logged in to access the profile page.')
            return redirect(url_for('main'))
        user_email = session['user_email']
        user_data = get_user_details_by_email(user_email)
        if not user_data:
            print('User not found in the database.')
            return redirect(url_for('main'))
        user_first_name = user_data['first_name']
        user_last_name = user_data['last_name']
        if request.method == 'POST' and 'submit' in request.form:
            if request.form['submit'] == 'Logout':
                session.pop('user_email', None)
                print('Logout successful')
                return redirect(url_for('main'))
        return render_template('profile_page.html', user_email=user_email, 
                               user_first_name=user_first_name, 
                               user_last_name=user_last_name)
    except Exception as e:
        print(str(e))
        return "An error occurred."


'''
Allow a user to log out of their account for security
'''
@app.route('/logout', methods=['POST'])
def logout():
    if 'user_email' in session:
        session.pop('user_email', None)  
        print('Logout successful')
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run()
