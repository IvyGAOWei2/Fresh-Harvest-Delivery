from app import app
from flask import render_template, request, session
from datetime import datetime

# User-defined function
from dbFile.config import insertSQL, updateSQL,fetchAll, fetchOne
from common import toDay, roleRequired

@app.route("/consumer/box", methods=['GET', 'POST'])
@roleRequired(['Consumer'])
def consumer_box():
    print(session['id'])
    list = fetchAll("SELECT * from Subscription where user_id = %s", (session['id'],), True)
    now = datetime.now()
    current_date = now.date()
    return render_template('consumer_box.html', subscription_list=list,  current_date=current_date)

