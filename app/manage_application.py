from app import app 

from flask import render_template, request, session, jsonify
from dbFile.config import updateSQL, fetchAll, fetchOne, insertSQL
from common import roleRequired
from datetime import datetime



@app.template_filter('dateformat')
def dateformat(value, format='%d/%m/%Y'):
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime(format)
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    except ValueError:
        return value

@app.route('/manage-applications')
@roleRequired(['Local_Manager','National_Manager'])
def manage_applications():
    applications = get_all_applications()
    return render_template('manage-applications.html', applications=applications)

def get_all_applications():
    query = "SELECT application_id, user_id, business_name, contact_name, email, phone, address, city, postcode, status, application_date, documentation FROM BusinessApplications"
    return fetchAll(query)

@app.route('/approve-application', methods=['POST'])
@roleRequired(['Local_Manager','National_Manager'])
def approve_application():
    application_id = request.form['application_id']
    update_application_status(application_id, 'Approved')
    user_id = get_user_id_from_application(application_id)
    update_user_type(user_id, 'Business')
    set_default_account_limit(user_id, 500) 
    return jsonify({"status": True})

def set_default_account_limit(user_id, limit):
    query = "UPDATE Consumer SET account_limit = %s WHERE user_id = %s"
    updateSQL(query, (limit, user_id))

@app.route('/reject-application', methods=['POST'])
@roleRequired(['Local_Manager','National_Manager'])
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


def get_business_accounts():
    query = """
    SELECT u.user_id, u.email, c.given_name, c.family_name, c.phone, c.account_limit 
    FROM Users u
    JOIN Consumer c ON u.user_id = c.user_id
    WHERE c.user_type = 'Business'
    """
    return fetchAll(query)

@app.route('/update-account-limit', methods=['POST'])
@roleRequired(['Local_Manager','National_Manager'])
def update_account_limit():
    user_id = request.form['userId']
    new_limit = request.form['accountLimit']
    
    query = "UPDATE Consumer SET account_limit = %s WHERE user_id = %s"
    updateSQL(query, (new_limit, user_id))
    
    return jsonify({"status": True})

@app.route('/profile/submitReviewRequest', methods=['POST'])
@roleRequired(['Consumer'])
def submitReviewRequest():
    data = request.get_json()
    user_id = data['user_id']
    new_account_limit = data['newAccountLimit']

    # Fetch current account limit
    current_limit_query = "SELECT account_limit FROM Consumer WHERE user_id = %s"
    current_account_limit = fetchOne(current_limit_query, (user_id,))[0]

    query = """
    INSERT INTO AccountLimitReviewRequests (user_id, current_account_limit, new_account_limit)
    VALUES (%s, %s, %s)
    """
    values = (user_id, current_account_limit, new_account_limit)
    insertSQL(query, values)

    return jsonify({"status": True})


@app.route('/admin/reviewRequests', methods=['GET'])
@roleRequired(['Local_Manager', 'National_Manager'])
def viewReviewRequests():
    query = """
    SELECT r.request_id, r.user_id, b.business_name, r.current_account_limit, r.new_account_limit, r.request_date, r.status, r.decision_date
    FROM AccountLimitReviewRequests r
    JOIN Consumer c ON r.user_id = c.user_id
    JOIN BusinessApplications b ON r.user_id = b.user_id
    WHERE c.user_type = 'Business'
    ORDER BY r.request_date DESC
    """
    requests = fetchAll(query)
    formatted_requests = [
        (
            req[0],
            req[1],
            req[2],
            req[3],
            req[4],
            req[5],
            req[6],
            req[7]
        )
        for req in requests
    ]

    return render_template('manage-credit-limit.html', requests=formatted_requests)
@app.route('/admin/decideReviewRequest', methods=['POST'])
@roleRequired(['Local_Manager','National_Manager'])
def decideReviewRequest():
    data = request.get_json()
    request_id = data['request_id']
    decision = data['decision']
    decision_date = datetime.now()

    if decision == 'Approved':
        query = "UPDATE Consumer c INNER JOIN AccountLimitReviewRequests r ON c.user_id = r.user_id SET c.account_limit = r.new_account_limit WHERE r.request_id = %s"
        updateSQL(query, (request_id,))
    
    query = "UPDATE AccountLimitReviewRequests SET status = %s, decision_date = %s WHERE request_id = %s"
    updateSQL(query, (decision, decision_date, request_id))

    return jsonify({"status": True})

