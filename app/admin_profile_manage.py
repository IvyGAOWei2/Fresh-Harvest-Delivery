from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import updateSQL,fetchAll
from common import roleRequired, getUserProfile, validateEmployeeProfile


@app.route("/admin/profiles")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def adminProfiles():
    print(session.get('type'))

    if session.get('type') in ['Consumer']:
        result = fetchAll("SELECT Users.email, Consumer.* FROM Consumer join Users on Consumer.user_id=Users.user_id where Users.type='Consumer';")

    elif session.get('type') in ['Staff']:
        result = fetchAll("""SELECT Users.email, Employees.*, Depots.location FROM Employees 
                          join Users on Employees.user_id=Users.user_id 
                          join Depots on Employees.depot_id=Depots.depot_id where Users.type='Staff';""")

    elif session.get('type') in ['Local_Manager']:
        result = fetchAll("""SELECT Users.email, Employees.*, Depots.location FROM Employees 
                          join Users on Employees.user_id=Users.user_id 
                          join Depots on Employees.depot_id=Depots.depot_id where Users.type='Local_Manager';""")

    return render_template('admin_profile_list.html', member_list=result,profile_type=session.get('type'))


# @app.route('/admin/profile/search',methods = ["GET","POST"])
# # @roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
# def profileSearch():

#     searchBy = request.get_json()['searchBy']
#     profile_type = request.get_json()['profile_type']

#     result = fetchAll("SELECT * FROM " + profile_type + " WHERE first_name LIKE %s \
#         OR last_name LIKE %s ORDER BY user_id ASC", ('%' + searchBy + '%','%' + searchBy + '%'))
#     return render_template('admin_profile_list.html', member_list=result, profile_type=profile_type)


@app.route("/admin/profile/update",methods = ["GET","POST"])
# @roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def admin_profile_update():
    if request.method == 'POST':   
    #     if request.values.get("update_member") == "update_member":
        test = request.form.get("member_new_password")
        print(request.form.get(test ,9999999999999999999999999999))
    return render_template('admin_profile_list.html')
    

# @app.route("/admin/profile/add",methods = ["GET","POST"])
# # @roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
# def admin_profile_add():
#     if request.values.get("add_member") == "add_member":
#         print(request.form.get("add_password",888888888888888888888) )

#     return render_template('admin_profile_list.html')


# @app.route("/admin/profile/delete",methods = ["GET","POST"])
# # @roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
# def admin_profile_delete():
#     pass
#     return render_template('admin_profile_list.html')