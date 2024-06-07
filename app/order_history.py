from app import app
from flask import render_template, request, session, redirect
from dbFile.config import fetchAll, updateSQL,fetchOne
# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile, getUserProfile



@app.route("/order/history")
@roleRequired(['Consumer'])
def orderHistory():
    orders = fetchAll("SELECT order_id, order_date, delivery_date, total, status FROM Orders WHERE user_id = %s;", (session['id'],), True)
    return render_template('order-history.html', orders=orders)



@app.route("/order/detail/<int:order_id>")
@roleRequired(['Consumer','Staff', 'Local_Manager', 'National_Manager'])
def orderDetail(order_id):
    
    order = fetchOne('SELECT * FROM Orders WHERE order_id = %s', (order_id,),True)
    exclusion_list = ",".join(str(pid) for pid in app.giftcard_list)
    
    products = fetchAll("SELECT o.*, p.name, p.price, pi.image  FROM OrderItems o JOIN Products p \
        ON o.product_id = p.product_id JOIN ProductImages pi ON p.product_id = pi.product_id \
        WHERE o.order_id = %s AND o.product_id NOT IN ("+ exclusion_list + ")", (order_id,), True)

    giftcards = fetchAll('SELECT gc.*, pi.image FROM GiftCards gc JOIN ProductImages pi ON \
        gc.product_id = pi.product_id WHERE gc.order_id = %s;', (order_id,),True)
    print(giftcards)
    if session['type'] == 'Consumer':
        return render_template('order-detail.html', orderProducts=products, Giftcards=giftcards,order=order, shipping=app.shipping)
    else:
        return render_template('manage-order-detail.html', orderProducts=products, Giftcards=giftcards,order=order, shipping=app.shipping)






@app.route("/admin/order/history", methods = ["GET", 'POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def staffOrderHistory():
    sql_orders = """
        SELECT 
            Orders.order_id, 
            Orders.order_date, 
            Orders.delivery_date, 
            Orders.total, 
            Orders.status,
            CONCAT(Consumer.given_name, ' ', Consumer.family_name) AS full_name
        FROM 
            Orders
        JOIN 
            Consumer ON Orders.user_id = Consumer.user_id;
"""
    orders = fetchAll(sql_orders, None, True)
    return render_template('manage-order-history.html', orders=orders)


@app.route("/admin/order/refund/", methods = ['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def staffRefund():
    data = request.get_json()
    order_item_id = data.get('order_item_id')
    if order_item_id:
        updateSQL("UPDATE OrderItems SET is_refunded = TRUE WHERE order_item_id = %s", (order_item_id,))
    return render_template('manage-order-detail.html')

@app.route("/admin/order/status/", methods = ['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def updateOrderStatus():
    data = request.get_json()
    order_id = data.get('order_id')
    new_status  = data.get('status')
    print(order_id)
    print(new_status)
    if not order_id or not new_status:
        return {"status": False, "error": "Missing order_id or status"}, 400
    
    update_successful = updateSQL("UPDATE Orders SET status = %s WHERE order_id = %s", (new_status, order_id))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500



