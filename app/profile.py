from app import app
from flask import render_template, request, session,request, jsonify,redirect, url_for

# User-defined function
from dbFile.config import updateSQL, fetchOne, insertSQL
from common import roleRequired, getUserProfile, validateEmployeeProfile, validateConsumerProfile
from werkzeug.utils import secure_filename
import os

@app.route("/profile/consumer")
@roleRequired(['Consumer'])
def profileConsumer():
    profile = getUserProfile(session['id'], session['type'])
    application_status = get_application_status(session['id'])
    print(profile)
    return render_template('profile-consumer.html', profile=profile, application_status=application_status)

def get_application_status(user_id):
    query = "SELECT status FROM BusinessApplications WHERE user_id = %s ORDER BY application_date DESC LIMIT 1"
    result = fetchOne(query, (user_id,))
    return result[0] if result else None

@app.route('/apply-business-account', methods=['GET', 'POST'])
@roleRequired(['Consumer'])
def apply_business_account():

    if request.method == 'POST':

        user_id = session['id']
        business_name = request.form['business_name']
        contact_name = request.form['contact_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        postcode = request.form['postcode']

        documentation = request.files['documentation']
        documentation_filename = secure_filename(documentation.filename)
        documentation_path = os.path.join(app.config['UPLOAD_FOLDER'], documentation_filename)
        os.makedirs(os.path.dirname(documentation_path), exist_ok=True)

        documentation.save(documentation_path)

        # Insert the application into the database
        insert_business_application(user_id, business_name, contact_name, email, phone, address, city, postcode, documentation_filename)

        return jsonify({"status": True, "redirect": url_for('profileConsumer')})

    return render_template('apply-business-account.html')

def insert_business_application(user_id, business_name, contact_name, email, phone, address, city, postcode, documentation_filename):
    query = """
    INSERT INTO BusinessApplications (user_id, business_name, contact_name, email, phone, address, city, postcode, documentation)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (user_id, business_name, contact_name, email, phone, address, city, postcode, documentation_filename)
    insertSQL(query, values)

@app.route("/profile/employee")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def profileEmployee():
    profile = getUserProfile(session['id'], session['type'])
    return render_template('profile-employee.html', profile=profile)

@app.route('/profile/update', methods=['POST'])
@roleRequired(['Consumer', 'Staff', 'Local_Manager', 'National_Manager'])
def profileUpdate():
    if session.get('type') in ['Consumer']:
        table_name = "Consumer"
        verified_data = validateConsumerProfile(request.get_json())
    else:
        table_name = "Employees"
        verified_data = validateEmployeeProfile(request.get_json())

    user_id = verified_data['user_id']
    verified_data.pop('user_id')

    if 'old_password' in verified_data and 'new_password' in verified_data:
        old_db_hash = fetchOne('SELECT password_hash FROM Users WHERE user_id = %s AND is_deleted = FALSE', (user_id,))
        if app.hashing.check_value(old_db_hash[0], verified_data['old_password'], salt=app.salt):
            new_hashed = app.hashing.hash_value(verified_data['new_password'], salt=app.salt)
            updateSQL("UPDATE Users SET password_hash = %s WHERE user_id = %s;", (new_hashed, user_id))
            [verified_data.pop(key) for key in ('old_password', 'new_password')]
            update_successful = 1
        else:
            return {"status": False, "message":"Incorrect old password, please try again."}, 500
    elif 'old_password' in verified_data:
        return {"status": False, "message":"Please enter your new password"}, 500
    elif 'new_password' in verified_data:
        return {"status": False, "message":"Please enter your old password"}, 500

    if verified_data:
        updates,params = [], []
        for key, value in verified_data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(user_id)

        update_successful = updateSQL("UPDATE " + table_name + " SET " + ", ".join(updates) + " WHERE user_id = %s", params)

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500