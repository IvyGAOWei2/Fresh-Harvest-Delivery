from app import app
from flask import jsonify, render_template, request, session
import os

# User-defined function
from dbFile.config import fetchOne, insertSQL, updateSQL, fetchAll
from common import getImageExt, generateImageId, roleRequired, validateEmail, validateRegisterEmployee, validateEmployeeProfile, validateConsumerProfile


# Function to save uploaded images
def saveImage(img):
    # Get the file extension of the uploaded image
    ext = getImageExt(img.filename)

    # Check if the extension is valid
    if not ext:
        return ext

    # Generate a unique image name using a custom function
    image_name = generateImageId() + '.' + ext
    # Construct the full path where the image will be saved
    filename = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

    # Save the uploaded image to the specified location
    img.save(filename)
    # Return the name of the saved image
    return 'upload/' + image_name


@app.route("/admin/profiles")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def adminProfiles():
    type = session['type']
    depot_id = session['depot_id']
    profile_type = request.args.get('profile_type')
    
    if depot_id == 6:
        if profile_type == "Consumer":
            result = fetchAll("SELECT Users.email, Consumer.* FROM Consumer \
                JOIN Users on Consumer.user_id=Users.user_id WHERE Users.type='Consumer' AND Users.is_deleted = FALSE;",None ,True)
        else:
            if session.get('type') in ['Local_Manager']:
                result = fetchAll("""SELECT Users.email, Users.type, Employees.* FROM Employees \
                    JOIN Users on Employees.user_id=Users.user_id WHERE Users.type='Staff' AND Users.is_deleted = FALSE;""",None ,True)
            else:
                result = fetchAll("""SELECT Users.email,Users.type, Employees.* FROM Employees \
                    JOIN Users ON Employees.user_id = Users.user_id \
                    WHERE (Users.type = 'Staff' OR Users.type = 'Local_Manager') AND Users.is_deleted = FALSE;""",None ,True)
    else:
        if profile_type == "Consumer":
            result = fetchAll("SELECT Users.email, Consumer.* FROM Consumer \
                JOIN Users on Consumer.user_id=Users.user_id WHERE Users.type='Consumer' and Users.depot_id=%s AND Users.is_deleted = FALSE;",(depot_id,) ,True)
        else:
            if session.get('type') in ['Local_Manager']:
                result = fetchAll("""SELECT Users.email, Users.type, Employees.* FROM Employees \
                    JOIN Users on Employees.user_id=Users.user_id WHERE Users.type='Staff' and Users.depot_id=%s AND Users.is_deleted = FALSE;""",(depot_id,) ,True)
            else:
                result = fetchAll("""SELECT Users.email,Users.type, Employees.* FROM Employees \
                    JOIN Users ON Employees.user_id = Users.user_id \
                    WHERE (Users.type = 'Staff' OR Users.type = 'Local_Manager') and Users.depot_id=%s AND Users.is_deleted = FALSE;""",(depot_id,) ,True)

                
    invoice = fetchAll("SELECT * from Invoices;",None ,True)

    return render_template('admin_profile_list.html', member_list=result, profile_type=profile_type, depotList=app.depot_list, type=type,invoice=invoice)


@app.route("/admin/profile/update", methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def adminProfileUpdate():
    if request.form.get('profile_type') == 'Consumer':
        table_name = "Consumer"
        verified_data = validateConsumerProfile({key: value for key, value in dict(request.form).items() if value})
    else:
        table_name = "Employees"
        verified_data = validateEmployeeProfile({key: value for key, value in dict(request.form).items() if value})
        print(verified_data,111 )
        employee_type = verified_data['type'] # get employee_type to update in Users
        verified_data.pop('type')

    # get new password to update in Users
    reset_password = 0
    if 'new_password' in verified_data:
        reset_password = verified_data['new_password'] # get new_password to update in Users
        verified_data.pop('new_password')

    user_id = verified_data['user_id'] 
    verified_data.pop('user_id')

    if verified_data:
        updates,params = [], []
        for key, value in verified_data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(user_id)
        print(updates,params,21212121212121)
        update_successful = updateSQL("UPDATE " + table_name + " SET " + ", ".join(updates) + " WHERE user_id = %s", tuple(params))
        # if depot_id changed, update Users
        depot_id = verified_data['depot_id'] 
        original_depot_id = fetchOne("select depot_id from Users where user_id=%s",(user_id,),withDescription=False)[0]
        if depot_id != original_depot_id:
            updateSQL("UPDATE Users set depot_id = %s WHERE user_id = %s;", (depot_id, user_id))

    image = request.files['image']
    if image.filename:
        image_name = saveImage(image)
        update_successful = updateSQL("UPDATE " + table_name + " SET image = %s WHERE user_id = %s;", (image_name, user_id))

    # if employee type change, update Users
    original_employee_type = fetchOne("select type from Users where user_id=%s",(user_id,),withDescription=False)[0]
    if original_employee_type != "Consumer" and original_employee_type != employee_type:
        update_successful = updateSQL("update Users set type=%s where user_id=%s",(employee_type,user_id))
      
    # if new password, update Users
    if reset_password != 0:
        new_hashed = app.hashing.hash_value(reset_password, salt=app.salt)
        print(new_hashed)
        updateSQL("UPDATE Users SET password_hash = %s WHERE user_id = %s;", (new_hashed, user_id))
        update_successful = 1
  
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
    employee_type = request.form.get("type")
  
    if not new_account:
        return {"status": False, 'message': 'Invalid register request !!!'}, 500

    if validateEmail(new_account.email):
        return {"status": False, 'message': 'Email ' + new_account.email + ' has already been used by another user'}, 200
    else:
        try:
            hashed = app.hashing.hash_value(new_account.password, salt=app.salt)
            if employee_type == "Staff":
                user_id = insertSQL("INSERT INTO Users (email, password_hash, depot_id, type) VALUES(%s,%s,%s,%s);", (new_account.email, hashed, new_account.depot_id, 'Staff'))
            elif employee_type == "Local_Manager":
                user_id = insertSQL("INSERT INTO Users (email, password_hash, depot_id, type) VALUES(%s,%s,%s,%s);", (new_account.email, hashed, new_account.depot_id, 'Local_Manager'))

            image = request.files['image']
            if image.filename:
                image_name = saveImage(image)
            insertSQL("INSERT INTO Employees (user_id, given_name, family_name, address, phone, hire_date, depot_id, image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);", \
            (user_id, new_account.given_name, new_account.family_name, new_account.address, new_account.phone, new_account.hire_date, new_account.depot_id,image_name))
        except:
            return {"status": False}, 500
        else:
            return {"status": True}, 200
        

@app.route("/admin/invoice",methods = ["POST"])
@roleRequired(['Staff','Local_Manager', 'National_Manager'])
def adminInvoice():
    invoice_id = request.form.get("invoice_id")
    is_paid = request.form.get("is_paid")
   
    if is_paid == "0":
        success = updateSQL("update Invoices set is_paid=1 where invoice_id=%s;",(invoice_id,))
        success = 1
    elif is_paid == "1":
        success = updateSQL("update Invoices set is_paid=0 where invoice_id=%s;",(invoice_id,))
        success = 1

    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})
    