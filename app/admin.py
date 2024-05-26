from app import app
from flask import render_template, request, session, jsonify

# User-defined function
from dbFile.config import updateSQL, fetchAll, fetchOne
from common import roleRequired, getUserProfile, validateEmployeeProfile, validateConsumerProfile


@app.route("/admin")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def admin():
    return render_template('admin.html')

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

@app.route("/admin/action")
@roleRequired(['Local_Manager', 'National_Manager'])
def adminAction():
    return render_template('admin-action.html')

@app.route('/manage-applications')
@roleRequired(['Local_Manager'])
def manage_applications():
    applications = get_all_applications()
    return render_template('manage-applications.html', applications=applications)

def get_all_applications():
    query = "SELECT application_id, user_id, business_name, contact_name, email, phone, address, city, postcode, status, application_date, documentation FROM BusinessApplications"
    return fetchAll(query)

@app.route('/approve-application', methods=['POST'])
@roleRequired(['Local_Manager'])
def approve_application():
    application_id = request.form['application_id']
    update_application_status(application_id, 'Approved')
    user_id = get_user_id_from_application(application_id)
    update_user_type(user_id, 'Business')
    return jsonify({"status": True})

@app.route('/reject-application', methods=['POST'])
@roleRequired(['Local_Manager'])
def reject_application():
    application_id = request.form['application_id']
    update_application_status(application_id, 'Rejected')
    return jsonify({"status": True})

def update_application_status(application_id, status):
    query = "UPDATE BusinessApplications SET status = %s WHERE application_id = %s"
    updateSQL(query, (status, application_id))

def get_user_id_from_application(application_id):
    query = "SELECT user_id FROM BusinessApplications WHERE application_id = %s"
    result = fetchOne(query, (application_id,))
    return result[0] if result else None

def update_user_type(user_id, user_type):
    query = "UPDATE Consumer SET user_type = %s WHERE user_id = %s"
    updateSQL(query, (user_type, user_id))

@app.route('/business-accounts')
@roleRequired(['Local_Manager'])
def business_accounts():
    accounts = get_business_accounts()
    return render_template('business-accounts.html', accounts=accounts)

def get_business_accounts():
    query = """
    SELECT u.user_id, u.email, c.given_name, c.family_name, c.phone, c.account_limit 
    FROM Users u
    JOIN Consumer c ON u.user_id = c.user_id
    WHERE c.user_type = 'Business'
    """
    return fetchAll(query)

@app.route('/update-account-limit', methods=['POST'])
@roleRequired(['Local_Manager'])
def update_account_limit():
    user_id = request.form['userId']
    new_limit = request.form['accountLimit']
    
    query = "UPDATE Consumer SET account_limit = %s WHERE user_id = %s"
    updateSQL(query, (new_limit, user_id))
    
    return jsonify({"status": True})