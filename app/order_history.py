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
    
    orders = fetchOne('SELECT * FROM Orders WHERE order_id = %s', (order_id,),True)
    # print(orders)
    order_items = fetchAll('SELECT * FROM OrderItems WHERE order_id = %s', (order_id,),True)
    gift_cards = fetchAll('SELECT * FROM GiftCards WHERE order_id = %s', (order_id,),True)
    # print(gift_cards) [{'gift_card_id': 1, 'product_id': 100, 'order_id': 1, 'code': 'DKFQN2E0', 'balance': '25', 'is_active': 0}]
    
    # divide order items as giftcard & normal products for two tables
    order_products = []
    order_giftcards = []
    
    for item in order_items:
        product = fetchOne('SELECT * FROM Products WHERE product_id = %s', (item['product_id'],),True)
        productImg = fetchOne('SELECT * FROM ProductImages WHERE product_id = %s', (item['product_id'],),True)
        # print(productImg)  {'product_image_id': 1, 'product_id': 1, 'image': 'Kiwifruit Green Fruit.png', 'is_primary': 1, 'is_deleted': 0}
        item['product_name'] = product['name']
        item['product_image'] = productImg['image']
        item['quantity'] = item['quantity']
        item['order_item_id'] = item['order_item_id']
        item['price'] = product['price']
        item['total'] = item['price'] * item['quantity']

        if item['product_id'] in [gift_card['product_id'] for gift_card in gift_cards]:
            # Append the gift card data to order_giftcards
            for card in gift_cards:
                if card['product_id'] == item['product_id']:
                    card['product_image'] = productImg['image']
                    card['code'] = card['code']
                    card['balance'] = card['balance']
                    card['is_active'] = card['is_active']
                    order_giftcards.append(card)
        else:
            order_products.append(item)
    print(order_products)
    print(order_giftcards)  # 打印后为空，因为OrderItems里没有对应giftcard的订单记录,giftcard单方面有orderid

    if session['type'] == 'Consumer':
        return render_template('order-detail.html', orderProducts=order_products, orderGiftcards=order_giftcards,orderDate= orders['order_date'], orderStatus= orders['status'], orderID= order_id)
    else:
        return render_template('manage-order-detail.html', orderProducts=order_products, orderGiftcards=order_giftcards,orderDate= orders['order_date'], orderStatus= orders['status'], orderID= order_id)






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



