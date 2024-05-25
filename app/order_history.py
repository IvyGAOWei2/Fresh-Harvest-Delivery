from app import app
from flask import render_template, request
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile



@app.route("/consumer/order/history", methods = ["GET"])
@roleRequired(['Consumer'])
def consumerOrderHistory():

  
    return render_template('consumer-order-history.html' )



@app.route("/staff/order/history", methods = ["GET"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def staffOrderHistory():

  
    return render_template('manage-order-history.html' )