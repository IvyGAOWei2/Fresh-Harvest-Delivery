from app import app
from flask import render_template


@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/checkout")
def checkout():
    return render_template('chackout.html')