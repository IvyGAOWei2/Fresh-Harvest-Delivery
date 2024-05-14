from app import app
from flask import render_template, redirect, url_for, session


@app.route("/")
def index():
    print(session)
    if 'loggedin' not in session or session.get('type') == 'Consumer':
        return render_template('index.html')
    else:
        return redirect(url_for('admin'))

@app.route("/404")
def notFound():
    return render_template('404.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/exmaples")
def exmaples():
    return render_template('exmaples.html')