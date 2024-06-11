from app import app
from flask import render_template, request, session,jsonify
import requests
# User-defined function
from dbFile.config import fetchAll, updateSQL, fetchOne, insertSQL
from common import roleRequired, emailOrder, toDay
from emailMethod.method import sendOrderStatus


@app.route("/order/history")
@roleRequired(['Consumer'])
def orderHistory():
    orders = fetchAll("SELECT order_id, order_date, delivery_date, total, shipping_fee, status FROM Orders WHERE user_id = %s;", (session['id'],), True)
    return render_template('order-history.html', orders=orders)


@app.route("/order/detail/<int:order_id>")
@roleRequired(['Consumer','Staff', 'Local_Manager', 'National_Manager'])
def orderDetail(order_id):
    order_sql = """
        SELECT Orders.*, 
        CONCAT(Consumer.given_name, ' ', Consumer.family_name) AS full_name 
        FROM Orders 
        JOIN Consumer ON Orders.user_id = Consumer.user_id 
        WHERE Orders.order_id = %s
"""
    order = fetchOne(order_sql, (order_id,),True)
    # print(order)
    exclusion_list = ",".join(str(pid) for pid in app.giftcard_list)

    products = fetchAll("SELECT o.*, p.name, p.price, pi.image FROM OrderItems o JOIN Products p \
        ON o.product_id = p.product_id JOIN ProductImages pi ON p.product_id = pi.product_id \
        WHERE o.order_id = %s AND o.product_id NOT IN ("+ exclusion_list + ")", (order_id,), True)

    if order['status'] == 'Pending':
        giftcards = fetchAll('SELECT gc.balance, gc.is_active, pi.image FROM GiftCards gc JOIN ProductImages pi ON \
            gc.product_id = pi.product_id WHERE gc.order_id = %s;', (order_id,),True)
    elif order['status'] == 'Cancelled':
        giftcards = fetchAll("SELECT o.*, p.name, p.price, pi.image FROM OrderItems o JOIN Products p \
            ON o.product_id = p.product_id JOIN ProductImages pi ON p.product_id = pi.product_id \
            WHERE o.order_id = %s AND o.product_id IN ("+ exclusion_list + ")", (order_id,), True)
    else:
        giftcards = fetchAll('SELECT gc.*, pi.image FROM GiftCards gc JOIN ProductImages pi ON \
            gc.product_id = pi.product_id WHERE gc.order_id = %s;', (order_id,),True)

    if session['type'] == 'Consumer':
        return render_template('order-detail.html', orderProducts=products, Giftcards=giftcards,order=order, shipping=app.shipping)
    else:
        return render_template('manage-order-detail.html', orderProducts=products, Giftcards=giftcards,order=order, shipping=app.shipping)


@app.route("/order/del", methods=['POST'])
@roleRequired(['Consumer'])
def orderDel():
    data = request.get_json()

    update_successful = updateSQL("UPDATE GiftCards SET order_id = NULL WHERE order_id = %s;", (data['order_id'],))
    update_successful = updateSQL("UPDATE Orders SET status = 'Cancelled' WHERE order_id = %s;", (data['order_id'],))

    # restore business account_available
    is_business = fetchOne('SELECT payment_method,total,shipping_fee FROM Orders WHERE order_id = %s', (data['order_id'],), True)

    if is_business['payment_method'] == 'Account':
        account_available =  fetchOne("SELECT account_available FROM Consumer WHERE user_id = %s;", (session['id'],))
        new_account_available = account_available[0] + is_business['total'] + is_business['shipping_fee']
        updateSQL("UPDATE Consumer SET account_available = %s WHERE user_id = %s;", (new_account_available, session['id']))

    # restore points
    isPointsRedeem = fetchOne('SELECT point_type, point_variation FROM ConsumerPoints WHERE order_id = %s', (data['order_id'],), True)
    if isPointsRedeem:
        point_variation = abs(isPointsRedeem['point_variation'])
        current_points = fetchOne('SELECT points FROM Consumer WHERE user_id = %s', (session['id'],))
        new_points = current_points[0] + point_variation

        insertSQL("INSERT INTO ConsumerPoints (user_id, order_id, point_type, point_variation, point_balance, point_date) \
                VALUES(%s,%s,%s,%s,%s,%s);", (session['id'], data['order_id'], 'Order Cancel', point_variation, new_points, toDay()))
        updateSQL("UPDATE Consumer SET points = %s WHERE user_id = %s;", (new_points, session['id']))

    if update_successful:
        order = emailOrder(data['order_id'])
        if app.send_email:
            sendOrderStatus(order['email'], data['order_id'], order['given_name'], order['order_date'], 'Cancelled')

        return {"status": True}, 200
    else:
        return {"status": False}, 500


@app.route("/order/reorder", methods=['POST'])
@roleRequired(['Consumer'])
def reorder():
    data = request.get_json()
    consumerCart = fetchOne("SELECT cart FROM Orders WHERE order_id = %s;", (data['order_id'],))

    return {"status": True, 'message': '/cart', 'cart': consumerCart}, 200


@app.route("/admin/order/history", methods = ["GET", 'POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def staffOrderHistory():
    sql_orders = """
        SELECT 
            Orders.order_id, 
            Orders.order_date, 
            Orders.delivery_date, 
            Orders.total,
            Orders.shipping_fee,
            Orders.status,
            CONCAT(Consumer.given_name, ' ', Consumer.family_name) AS full_name,
            Consumer.user_type
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
        return {'success': True}
    return {'success': False, 'message': 'Order item ID not provided'}

@app.route("/admin/order/status/", methods = ['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def updateOrderStatus():
    data = request.get_json()
    order = emailOrder(data['order_id'])


    # url = "https://api.hcconsulting.co.nz/citycentral/contact"
    # data = {'key1': 'value1','key2': 'value2'}
    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url, json=data, headers=headers)

    # print(response)
    # return {"status": False}, 500

    if data['status'] == 'Comfirmed':
        target_order = fetchOne('SELECT total, user_id, order_date FROM Orders WHERE order_id = %s', (data['order_id'],), True)
        current_points = fetchOne('SELECT points FROM Consumer WHERE user_id = %s', (target_order['user_id'],))
        variation = target_order['total']
        new_points = current_points[0] + variation

        insertSQL("INSERT INTO ConsumerPoints (user_id, order_id, point_type, point_variation, point_balance, point_date) \
            VALUES(%s,%s,%s,%s,%s,%s);", (target_order['user_id'], data['order_id'], 'Order Purchase', variation, new_points, target_order['order_date']))
        updateSQL("UPDATE Consumer SET points = %s WHERE user_id = %s;", (new_points, target_order['user_id']))

    update_successful = updateSQL("UPDATE Orders SET status = %s WHERE order_id = %s", (data['status'], data['order_id']))

    if update_successful:
        if app.send_email:
            sendOrderStatus(order['email'], data['order_id'], order['given_name'], order['order_date'], data['status'])
        return {"status": True}, 200
    else:
        return {"status": False}, 500