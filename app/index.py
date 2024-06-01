from app import app
from flask import render_template, session, request

from emailMethod.method import sendFhdContact

@app.route("/")
def index():
    print(session)
    return render_template('index.html')

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