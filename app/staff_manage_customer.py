from app import app
from flask import render_template


@app.route("/staff/manage/customer")
def staff_manage_customer():
    return render_template('staff_manage_customer.html')