from app import app
from flask import render_template, session, request
import json
from decimal import Decimal

# User-defined function
from dbFile.config import insertSQL, updateSQL, fetchOne, fetchAll
from common import roleRequired, toDay
from emailMethod.method import sendOrderStatus


@app.route("/cart")
@roleRequired(['Consumer'])
def cart():
    points = fetchOne('SELECT points FROM Consumer WHERE user_id = %s', (session['id'],))
    # print(points)
    return render_template('cart.html', shipping=app.shipping, points=points[0])

@app.route("/cart/update", methods = ["POST"])
@roleRequired(['Consumer'])
def cartUpdate():
    data = json.dumps(request.get_json())
    try:
        insertSQL("INSERT INTO ConsumerCart (user_id, cart) VALUES (%s, %s);", (session['id'], data))
    except:
        updateSQL("UPDATE ConsumerCart SET cart = %s WHERE user_id = %s;", (data, session['id']))

    return {"status": True}, 200


@app.route("/checkout", methods=['GET','POST'])
@roleRequired(['Consumer'])
def checkout():
    if request.method == 'POST':
        order = (request.get_json())

        order_id = insertSQL("INSERT INTO Orders (user_id, order_date, billing_address, delivery_address, cart, payment_method, payment_info, payment_status) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(session['id'], toDay(), json.dumps(order['billingform']), json.dumps(order['deliveryform']), json.dumps(order['cart']), order['paymentform']['paymentMethod'], order['paymentform']['payment_info'], 'Completed'))

        total_price = 0
        for product in order['cart']:
            if int(product['id'] )in app.giftcard_list:
                for i in range(int(product['qty'])):
                    updateSQL("UPDATE GiftCards SET order_id = %s WHERE gift_card_id = ( SELECT gift_card_id FROM \
                    (SELECT gift_card_id FROM GiftCards WHERE order_id IS NULL AND product_id = %s LIMIT 1) \
                    AS subquery);", (order_id, product['id']))

            price = fetchOne("SELECT price, unit_id FROM Products WHERE product_id = %s;", (product['id'],), True)
            if price['unit_id'] == 5:
                subtotal = price['price'] * (product['qty']*Decimal(0.25))
            else:
                subtotal = price['price'] * product['qty']
            insertSQL("INSERT INTO OrderItems (order_id, product_id, quantity, subtotal) VALUES \
                (%s,%s,%s,%s);",(order_id, product['id'], product['qty'], subtotal))
            total_price += subtotal

        shipping_fee = 0 if total_price > app.shipping else app.shipping
        update_successful = updateSQL("UPDATE Orders SET total = %s, shipping_fee = %s WHERE order_id = %s;", \
            (total_price, shipping_fee, order_id))
        
        if order['paymentform']['paymentMethod'] == 'Account':
            account_available =  fetchOne("SELECT account_available FROM Consumer WHERE user_id = %s;", (session['id'],))
            new_account_available = account_available[0] - total_price - shipping_fee
            updateSQL("UPDATE Consumer SET account_available = %s WHERE user_id = %s;", (new_account_available, session['id']))

        if update_successful:
            if order['finalTotal']['pointsUsed'] > 0:
                # new ConsumerPoints
                current_points = fetchOne('SELECT points FROM Consumer WHERE user_id = %s', (session['id'],))
                new_points =  -order['finalTotal']['pointsUsed'] + float(current_points[0])
                insertSQL("INSERT INTO ConsumerPoints (user_id, order_id, point_type, point_variation, point_balance, point_date) \
                    VALUES(%s,%s,%s,%s,%s,%s);", (session['id'], order_id,'Points Redeem', -order['finalTotal']['pointsUsed'], new_points, toDay()))     
                # update Consumer points
                updateSQL("UPDATE Consumer SET points = %s WHERE user_id = %s;", (new_points, session['id']))

            updateSQL("UPDATE ConsumerCart SET cart = %s WHERE user_id = %s;", ('[]', session['id'],))
            if app.send_email:
                sendOrderStatus(order['billingform']['email'], order_id, order['billingform']['given_name'], toDay(), 'Pending')
            return {"status": True, 'message': '/order/history'}, 200
        else:
            return {"status": False}, 500

    checkout_profile = fetchOne('SELECT given_name, family_name, address, postcode, phone, account_available, user_type FROM Consumer WHERE user_id = %s', (session['id'],), True)
    return render_template('chackout.html', checkoutProfile=checkout_profile, shipping=app.shipping)