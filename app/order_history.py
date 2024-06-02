from app import app
from flask import render_template, request, session
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile, getUserProfile



@app.route("/order/history")
@roleRequired(['Consumer'])
def orderHistory():
    orders = fetchAll("SELECT order_id, order_date, delivery_date, total, status FROM Orders WHERE user_id = %s;", (session['id'],), True)
    return render_template('order-history.html', orders=orders)

@app.route("/order/detail")
@roleRequired(['Consumer'])
def orderDetail():
    orders = fetchAll("SELECT order_id, order_date, delivery_date, total, status FROM Orders WHERE user_id = %s;", (session['id'],), True)
    return render_template('order-detail.html', orders=orders)





@app.route("/admin/order/history", methods = ["GET", 'POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def staffOrderHistory():
    orders = fetchAll("SELECT order_id, order_date, delivery_date, total, status FROM Orders;", None, True)
    return render_template('manage-order-history.html', orders=orders)

