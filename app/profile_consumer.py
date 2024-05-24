from app import app
from flask import render_template, session,request, jsonify,redirect, url_for
from werkzeug.utils import secure_filename
import os

# User-defined function
from dbFile.config import updateSQL, insertSQL,fetchOne
from common import roleRequired, getUserProfile, validateEmployeeProfile

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