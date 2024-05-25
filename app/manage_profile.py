from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import insertSQL, updateSQL, fetchAll
from common import roleRequired, validateEmail, validateRegisterEmployee, validateEmployeeProfile, validateConsumerProfile

@app.route("/admin/profiles")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def adminProfiles():
    profile_type = request.args.get('profile_type')
    if profile_type == "Consumer":
        result = fetchAll("SELECT Users.email, Consumer.* FROM Consumer \
            JOIN Users on Consumer.user_id=Users.user_id WHERE Users.type='Consumer' AND Users.is_deleted = FALSE;",None ,True)
    else:
        if session.get('type') in ['Local_Manager']:
            result = fetchAll("""SELECT Users.email, Employees.* FROM Employees \
                JOIN Users on Employees.user_id=Users.user_id WHERE Users.type='Staff' AND Users.is_deleted = FALSE;""",None ,True)
        else:
            result = fetchAll("""SELECT Users.email, Employees.* FROM Employees \
                JOIN Users ON Employees.user_id = Users.user_id \
                WHERE Users.type = 'Staff' OR Users.type = 'Local_Manager' AND Users.is_deleted = FALSE;""",None ,True)

    return render_template('admin_profile_list.html', member_list=result, profile_type=profile_type, depotList=app.depot_list)


@app.route('/admin/profile/search',methods = ["GET","POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def profileSearch():

    searchBy = request.get_json()['searchBy']
    profile_type = request.get_json()['profile_type']

    result = fetchAll("SELECT * FROM " + profile_type + " WHERE first_name LIKE %s \
        OR last_name LIKE %s ORDER BY user_id ASC", ('%' + searchBy + '%','%' + searchBy + '%'))
    return render_template('admin_profile_list.html', member_list=result, profile_type=profile_type)


@app.route("/admin/profile/update", methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def adminProfileUpdate():
    # need password futcion
    if request.form.get('profile_type') == 'Consumer':
        table_name = "Consumer"
        verified_data = validateConsumerProfile({key: value for key, value in dict(request.form).items() if value})
    else:
        table_name = "Employees"
        verified_data = validateEmployeeProfile({key: value for key, value in dict(request.form).items() if value})

    user_id = verified_data['user_id']
    verified_data.pop('user_id')

    if verified_data:
        updates,params = [], []
        for key, value in verified_data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(user_id)

    update_successful = updateSQL("UPDATE " + table_name + " SET " + ", ".join(updates) + " WHERE user_id = %s", tuple(params))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500

@app.route("/admin/profile/delete", methods = ["POST"])
@roleRequired(['Local_Manager', 'National_Manager'])
def adminProfileDel():
    data = request.get_json()
    update_successful = updateSQL("UPDATE Users SET is_deleted = TRUE WHERE user_id = %s;", (data['user_id'],))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500


@app.route("/admin/profile/add",methods = ["POST"])
@roleRequired(['Local_Manager', 'National_Manager'])
def adminProfileAdd():
    new_account = validateRegisterEmployee(request.form.to_dict())

    if not new_account:
        return {"status": False, 'message': 'Invalid register request !!!'}, 500

    if validateEmail(new_account.email):
        return {"status": False, 'message': 'Email ' + new_account.email + ' has already been used by another user'}, 200
    else:
        try:
            hashed = app.hashing.hash_value(new_account.password, salt=app.salt)
            user_id = insertSQL("INSERT INTO Users (email, password_hash, depot_id, type) VALUES(%s,%s,%s,%s);", (new_account.email, hashed, new_account.depot_id, 'Staff'))

            insertSQL("INSERT INTO Employees (user_id, given_name, family_name, address, phone, hire_date, depot_id, image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);", \
            (user_id, new_account.given_name, new_account.family_name, new_account.address, new_account.phone, new_account.hire_date, new_account.depot_id, 'user_default_image.png'))
        except:
            return {"status": False}, 500
        else:
            return {"status": True}, 200