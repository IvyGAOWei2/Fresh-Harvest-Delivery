from app import app
from flask import render_template, session

# User-defined function
from common import getUserProfile


@app.route("/admin")
def admin():
    profile = getUserProfile(session['id'], session['type'])
    return render_template('admin.html', profile=profile)

@app.route("/profile/employee")
def profileEmployee():
    profile = getUserProfile(session['id'], session['type'])
    return render_template('profile-employee.html', profile=profile)

@app.route("/admin/action")
def adminAction():
    return render_template('admin-action.html')