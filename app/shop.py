from app import app
from flask import render_template


@app.route("/shop")
def shop():
    return render_template('shop.html')


@app.route("/shopdetail")
def shopDetail():
    return render_template('shop-detail.html')

