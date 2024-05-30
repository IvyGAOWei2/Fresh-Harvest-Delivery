from app import app
from flask import render_template, session, request
import json

# User-defined function
from dbFile.config import insertSQL, updateSQL, fetchOne
from common import roleRequired


@app.route("/cart")
@roleRequired(['Consumer', 'Staff', 'Local_Manager', 'National_Manager'])
def cart():
    return render_template('cart.html')

@app.route("/cart/update", methods = ["POST"])
@roleRequired(['Consumer', 'Staff', 'Local_Manager', 'National_Manager'])
def cartUpdate():
    data = json.dumps(request.get_json())
    try:
        insertSQL("INSERT INTO ConsumerCart (user_id, cart) VALUES (%s, %s);", (session['id'], data))
    except:
        updateSQL("UPDATE ConsumerCart SET cart = %s WHERE user_id = %s;", (data, session['id']))

    return {"status": False}, 500


@app.route("/checkout")
@roleRequired(['Consumer', 'Staff', 'Local_Manager', 'National_Manager'])
def checkout():
    checkout_profile = fetchOne('SELECT given_name, family_name, address, postcode, phone FROM Consumer WHERE user_id = %s', (session['id'],), True)
    return render_template('chackout.html', checkoutProfile=checkout_profile)