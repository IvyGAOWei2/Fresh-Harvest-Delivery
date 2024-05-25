from app import app
from flask import render_template, redirect, url_for, request, session

# User-defined function
from dbFile.config import insertSQL
from common import validateLogin, validateUserAccount, validateRegister, validateEmail


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
        if request.method == 'POST':
            new_account = validateRegister(request.form.to_dict())

            if not new_account:
                return {"status": False, 'message': 'Invalid register request !!!'}, 500

            if validateEmail(new_account.email):
                return {"status": False, 'message': 'Email ' + new_account.email + ' has already been used by another user'}, 200
            else:
                hashed = app.hashing.hash_value(new_account.password, salt=app.salt)
                user_id = insertSQL("INSERT INTO Users (email, password_hash, depot_id) VALUES(%s,%s,%s);", (new_account.email, hashed, new_account.depot_id))

                insertSQL("INSERT INTO Consumer (user_id, given_name, family_name, address, phone, postcode, depot_id, image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);", \
                (user_id, new_account.given_name, new_account.family_name, new_account.address, new_account.phone, new_account.postcode, new_account.depot_id, 'user_default_image.png'))

                return {"status": True, 'message': '/registered'}, 200

        return render_template('register.html')

@app.route('/registered')
def registered():
    return render_template("registered.html")

@app.route('/password/reset', methods=['GET','POST'])
def passwordReset():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        return redirect(url_for('notFound'))
    return render_template('password-reset.html')