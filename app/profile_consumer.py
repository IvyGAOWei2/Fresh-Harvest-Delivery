from app import app
from flask import render_template, session

# User-defined function
from dbFile.config import updateSQL
from common import roleRequired, getUserProfile, validateEmployeeProfile

@app.route("/profile/consumer")
@roleRequired(['Consumer'])
def profileConsumer():
    profile = getUserProfile(session['id'], session['type'])
    print(profile)
    return render_template('profile-consumer.html', profile=profile)