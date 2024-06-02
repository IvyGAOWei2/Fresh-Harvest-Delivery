from app import app
from flask import render_template, session

# User-defined function
from dbFile.config import updateSQL, fetchOne


@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/checkout")
def checkout():
    checkout_profile = fetchOne('SELECT given_name, family_name, address, postcode, phone FROM Consumer WHERE user_id = %s', (session['id'],), True)
    return render_template('chackout.html', checkoutProfile=checkout_profile)