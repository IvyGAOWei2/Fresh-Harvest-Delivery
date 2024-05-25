from app import app
from flask import render_template

# User-defined function
from common import roleRequired


@app.route("/admin")
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def admin():
    return render_template('admin.html')

@app.route("/admin/action")
@roleRequired(['Local_Manager', 'National_Manager'])
def adminAction():
    return render_template('admin-action.html')