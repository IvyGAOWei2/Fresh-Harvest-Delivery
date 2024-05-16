from flask import Flask, render_template, request

from app import app

@app.route('/password/reset')
def reset_password():
    return render_template('password_reset.html')

@app.route('/reset', methods=['POST'])
def reset():
    email = request.form['email']
    return "Password reset link has been sent to {}".format(email)


