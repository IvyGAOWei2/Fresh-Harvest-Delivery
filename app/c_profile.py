from app import app
from flask import render_template

@app.route("/customer/profile")
def get_profile():
    return render_template('c_profile.html')