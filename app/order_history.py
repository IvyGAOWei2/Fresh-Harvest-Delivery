from app import app
from flask import render_template, request, session
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile, getUserProfile



@app.route("/order/history", methods = ["GET",'POST'])
@roleRequired(['Consumer'])
def orderHistory():
    profile = getUserProfile(session['id'], session['type'])

  
    return render_template('order-history.html', profile=profile )



@app.route("/admin/order/history", methods = ["GET", 'POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def staffOrderHistory():

  
    return render_template('manage-order-history.html' )