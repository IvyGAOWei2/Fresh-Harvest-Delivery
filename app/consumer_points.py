from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import updateSQL,fetchAll
from common import roleRequired, getUserProfile, validateEmployeeProfile

@app.route("/consumer/points", methods=['GET', 'POST'])
@roleRequired(['Consumer'])
def consumer_points():
    profile = getUserProfile(session['id'], session['type'])
    if request.method == "POST":
        gift_card_id= request.form.get("gift_card_id")
        print(gift_card_id)
    return render_template('consumer_points.html', profile=profile)
    