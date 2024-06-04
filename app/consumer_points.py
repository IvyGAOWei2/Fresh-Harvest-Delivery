from app import app
from flask import render_template, request, session

# User-defined function
from dbFile.config import insertSQL, updateSQL,fetchAll, fetchOne
from common import toDay, roleRequired

@app.route("/consumer/points", methods=['GET', 'POST'])
@roleRequired(['Consumer'])
def consumer_points():
    points_balance = fetchOne('SELECT points FROM Consumer WHERE user_id = %s', (session['id'],))
    points_history = fetchAll("SELECT order_id,gift_card_id,point_type,point_variation,point_balance,point_date \
        FROM ConsumerPoints WHERE user_id = %s AND is_active = True", (session['id'],), True)

    return render_template('consumer_points.html', pointsBalance=points_balance[0], pointsHistory=points_history)

@app.route("/giftcard/redeem", methods=['POST'])
@roleRequired(['Consumer'])
def giftcardRedeem():
    code = request.form.to_dict()['code']

    if len(code) == 8:
        update_successful = updateSQL("UPDATE GiftCards SET is_active = True WHERE code = %s;", (code,))

    if update_successful:
        current_points = fetchOne('SELECT points FROM Consumer WHERE user_id = %s', (session['id'],))
        gift_card = fetchOne('SELECT balance, gift_card_id FROM GiftCards WHERE code = %s', (code,), True)
        variation = float(gift_card['balance'])
        new_points = float(current_points[0]) + variation
        # new ConsumerPoints 
        insertSQL("INSERT INTO ConsumerPoints (user_id, gift_card_id, point_type, point_variation, point_balance, point_date) \
            VALUES(%s,%s,%s,%s,%s,%s);", (session['id'], gift_card['gift_card_id'], 'Gift Card', variation, new_points, toDay()))
        # update Consumer points
        updateSQL("UPDATE Consumer SET points = %s WHERE user_id = %s;", (new_points, session['id']))
        return {"status": True}, 200
    else:
        return {"status": False, 'message': 'The gift card code is incorrect or has already been used'}, 500