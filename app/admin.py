from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import updateSQL
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