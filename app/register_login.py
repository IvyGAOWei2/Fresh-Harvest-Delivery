from app import app
from flask import render_template


@app.route("/register/login")
def register_login():
    return render_template('register_login.html')




