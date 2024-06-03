from app import app 

from flask import render_template, request, session, jsonify
from dbFile.config import updateSQL, fetchAll, fetchOne, insertSQL
from common import roleRequired
from datetime import datetime
from collections import defaultdict

@app.route('/manage-applications')
@roleRequired(['Local_Manager', 'National_Manager'])
def manage_applications():
    try:
        user_role = session['type']

        if user_role == 'National_Manager':
            sql_applications = """
                SELECT a.application_id, a.user_id, a.business_name, a.contact_name, a.email, a.phone, a.address, a.city, a.postcode, a.status, a.application_date, a.documentation, c.depot_id
                FROM BusinessApplications a
                JOIN Consumer c ON a.user_id = c.user_id
                ORDER BY a.application_date DESC
            """
            applications = fetchAll(sql_applications)

            sql_depots = "SELECT depot_id, location FROM Depots"
            depots = fetchAll(sql_depots)
        else:
            depot_id = session['depot_id']
            sql_applications = """
                SELECT a.application_id, a.user_id, a.business_name, a.contact_name, a.email, a.phone, a.address, a.city, a.postcode, a.status, a.application_date, a.documentation, c.depot_id
                FROM BusinessApplications a
                JOIN Consumer c ON a.user_id = c.user_id
                WHERE c.depot_id = %s
                ORDER BY a.application_date DESC
            """
            applications = fetchAll(sql_applications, (depot_id,))
            depots = []

        formatted_applications = [
            (
                app[0],
                app[1],
                app[2],
                app[3],
                app[4],
                app[5],
                app[6],
                app[7],
                app[8],
                app[9],
                app[10],
                app[11],
                app[12]
            )
            for app in applications
        ]

        return render_template('manage-applications.html', applications=formatted_applications, depots=depots, user_role=user_role)
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/approve-application', methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def approve_application():
    application_id = request.form['application_id']
    update_application_status(application_id, 'Approved')
    user_id = get_user_id_from_application(application_id)
    update_user_type(user_id, 'Business')
    set_default_account_limit(user_id, 500)
    return jsonify({"status": True})

@app.route('/reject-application', methods=['POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def reject_application():
    application_id = request.form['application_id']
    update_application_status(application_id, 'Rejected')
    return jsonify({"status": True})

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

def set_default_account_limit(user_id, limit):
    query = "UPDATE Consumer SET account_limit = %s WHERE user_id = %s"
    updateSQL(query, (limit, user_id))

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
    try:
        user_role = session['type']

        if user_role == 'National_Manager':
            sql_requests = """
                SELECT r.request_id, r.user_id, b.business_name, r.current_account_limit, r.new_account_limit, r.request_date, r.status, r.decision_date, c.depot_id
                FROM AccountLimitReviewRequests r
                JOIN Consumer c ON r.user_id = c.user_id
                JOIN BusinessApplications b ON r.user_id = b.user_id
                WHERE c.user_type = 'Business'
                ORDER BY r.request_date DESC
            """
            requests = fetchAll(sql_requests)

            sql_depots = "SELECT depot_id, location FROM Depots"
            depots = fetchAll(sql_depots)
        else:
            depot_id = session['depot_id']
            sql_requests = """
                SELECT r.request_id, r.user_id, b.business_name, r.current_account_limit, r.new_account_limit, r.request_date, r.status, r.decision_date, c.depot_id
                FROM AccountLimitReviewRequests r
                JOIN Consumer c ON r.user_id = c.user_id
                JOIN BusinessApplications b ON r.user_id = b.user_id
                WHERE c.user_type = 'Business' AND c.depot_id = %s
                ORDER BY r.request_date DESC
            """
            requests = fetchAll(sql_requests, (depot_id,))
            depots = []

        grouped_requests = defaultdict(list)
        for req in requests:
            grouped_requests[req[1]].append(req)

        latest_requests = [max(group, key=lambda x: x[5]) for group in grouped_requests.values()]

        formatted_latest_requests = [
            (
                req[0],
                req[1],
                req[2],
                req[3],
                req[4],
                req[5],
                req[6],
                req[7],
                req[8]
            )
            for req in latest_requests
        ]

        return render_template('manage-credit-limit.html', requests=formatted_latest_requests, grouped_requests=grouped_requests, depots=depots, user_role=user_role)
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500