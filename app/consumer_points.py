from app import app
from flask import render_template, session

# User-defined function
from dbFile.config import updateSQL,fetchAll
from common import roleRequired, getUserProfile, validateEmployeeProfile

@app.route("/consumer/points")
@roleRequired(['Consumer'])
def consumer_points():
    profile = getUserProfile(session['id'], session['type'])

    
    return render_template('consumer_points.html', profile=profile)