from app import app
from flask import render_template, session, request
from common import fetchOne
from emailMethod.method import sendFhdContact

@app.route("/")
def index():
    print(session)
    sql = "SELECT description, discount_rate FROM Discounts WHERE status = 1 ORDER BY start_date DESC LIMIT 1"
    discount = fetchOne(sql, [])

    # Ensure discount is not None and extract the description and discount rate
    discount_description = discount[0] if discount else 'No current discounts available.'
    discount_rate = discount[1] if discount else '0%'

    return render_template('index.html', discount={'description': discount_description, 'rate': f'{discount_rate} OFF'})

@app.route("/404")
def notFound():
    return render_template('404.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        data = request.form.to_dict()
        sendFhdContact(data['name'], data['email'], data['type'], data['msg'])
        return {"status": False}, 404
    return render_template('contact.html')

@app.route("/exmaples")
def exmaples():
    return render_template('exmaples.html')