from app import app
from flask import render_template, redirect, url_for, request, session

# User-defined function
from common import validateLogin, validateUserAccount


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = validateLogin(request.form)

        if not login:
            return {"status": False, 'message': 'Invalid login request !!!'}, 500

        # Check if the user account exists
        account = validateUserAccount(login.email)

        if account:
            # Check if the user account is disabled
            if account['is_active'] == False:
                return {"status": False, 'message': login.email + ' is disabled'}, 200
            else:
                password_hash = account['password_hash']

            # Check if the password provided matches the hashed password in the database
            if app.hashing.check_value(password_hash, login.password, salt=app.salt):
                # If the password is correct, set session variables and redirect to the dashboard
                session['loggedin'], session['id'], session['email'], session['type'] = True, account['user_id'], account['email'], account['type']
                if account['type'] == 'Consumer':
                    return {"status": True, 'message': '/'}, 200
                else:
                    return {"status": True, 'message': '/admin'}, 200
            else:
                # If the password is incorrect, return an error message
                return {"status": False, 'message': 'User password is Incorrect'}, 200
        else:
            # If the user account does not exist, return an error message
            return {"status": False, 'message': login.email + ' not found'}, 404

    if session.get('loggedin'):
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('loggedin'):
        # Remove session data
        [session.pop(key, None) for key in ['loggedin', 'id', 'email', 'type']]
    return redirect(url_for('index'))

@app.route("/register", methods=['GET','POST'])
def register():
    if session.get('loggedin'):
        return redirect(url_for('index'))
    else:
        return render_template('register.html')