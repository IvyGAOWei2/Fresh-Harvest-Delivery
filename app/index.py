from app import app
from flask import render_template


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/404")
def notFound():
    return render_template('404.html')
