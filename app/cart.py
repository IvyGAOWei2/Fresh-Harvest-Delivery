from app import app
from flask import render_template, session, request
import json

# User-defined function
from dbFile.config import insertSQL, updateSQL, fetchOne
from common import roleRequired, toDay
from emailMethod.method import sendOrderStatus


@app.route("/cart")
@roleRequired(['Consumer'])
def cart():
    return render_template('cart.html')

@app.route("/cart/update", methods = ["POST"])
@roleRequired(['Consumer'])
def cartUpdate():
    data = json.dumps(request.get_json())
    try:
        insertSQL("INSERT INTO ConsumerCart (user_id, cart) VALUES (%s, %s);", (session['id'], data))
    except:
        updateSQL("UPDATE ConsumerCart SET cart = %s WHERE user_id = %s;", (data, session['id']))

    return {"status": False}, 500


@app.route("/checkout", methods=['GET','POST'])
@roleRequired(['Consumer'])
def checkout():
    if request.method == 'POST':
        order = (request.get_json())

        order_id = insertSQL("INSERT INTO Orders (user_id, order_date, billing_address, delivery_address, payment_method, payment_info, payment_status) \
            VALUES (%s,%s,%s,%s,%s,%s,%s);",(session['id'], toDay(), json.dumps(order['billingform']), json.dumps(order['deliveryform']), order['paymentform']['paymentMethod'], order['paymentform']['payment_info'], 'Completed'))

        total_price = 0
        for product in order['cart']:
            price = fetchOne("SELECT price FROM Products WHERE product_id = %s;", (product['id'],))
            subtotal = price[0] * product['qty']
            insertSQL("INSERT INTO OrderItems (order_id, product_id, quantity, subtotal) VALUES \
                (%s,%s,%s,%s);",(order_id, product['id'], product['qty'], subtotal))
            total_price += subtotal
        
        update_successful = updateSQL("UPDATE Orders SET total = %s WHERE order_id = %s;", (total_price, order_id))

        if update_successful:
            updateSQL("UPDATE ConsumerCart SET cart = %s WHERE user_id = %s;", ('[]', session['id'],))
            # sendOrderStatus(order['billingform']['email'], order_id, order['billingform']['given_name'], toDay(), 'Pending')
            return {"status": True, 'message': '/order/history'}, 200
        else:
            return {"status": False}, 500

    checkout_profile = fetchOne('SELECT given_name, family_name, address, postcode, phone, account_available, user_type FROM Consumer WHERE user_id = %s', (session['id'],), True)
    return render_template('chackout.html', checkoutProfile=checkout_profile)