from app import app
from flask import render_template

# User-defined function
from dbFile.config import updateSQL,fetchAll
from common import roleRequired, getUserProfile, validateEmployeeProfile


@app.route("/admin/manage/profile/<profile_type>",methods = ["GET","POST"])
# @roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def admin_manage_profile(profile_type):
    
    if profile_type == 'Consumer':
        result = fetchAll("SELECT Users.email, Consumer.* FROM Consumer join Users on Consumer.user_id=Users.user_id where Users.type='Consumer';")
        profile_type = 'Consumer'

    elif profile_type == 'Staff':
        result = fetchAll("""SELECT Users.email, Employees.*, Depots.location FROM Employees 
                          join Users on Employees.user_id=Users.user_id 
                          join Depots on Employees.depot_id=Depots.depot_id where Users.type='Staff';""")
        profile_type = 'Staff'

    elif profile_type == 'Local_Manager':
        result = fetchAll("""SELECT Users.email, Employees.*, Depots.location FROM Employees 
                          join Users on Employees.user_id=Users.user_id 
                          join Depots on Employees.depot_id=Depots.depot_id where Users.type='Local_Manager';""")
        profile_type = 'Local manager'

    return render_template('admin_manage_profile.html', member_list=result,profile_type=profile_type)