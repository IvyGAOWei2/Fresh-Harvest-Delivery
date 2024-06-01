from app import app
from flask import render_template, request, session, jsonify

# User-defined function
from dbFile.config import updateSQL, fetchAll, fetchOne
from common import roleRequired, getUserProfile, validateEmployeeProfile, validateConsumerProfile


@app.route("/admin")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def admin():
    return render_template('admin.html')

@app.route("/admin/action")
@roleRequired(['Local_Manager', 'National_Manager'])
def adminAction():
    return render_template('admin-action.html')

