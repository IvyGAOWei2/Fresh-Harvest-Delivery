from app import app, shop
from flask import render_template, request, session

# User-defined function
from dbFile.config import fetchOne, insertSQL, updateSQL, fetchAll
from common import roleRequired, validateEmail, validateRegisterEmployee, validateEmployeeProfile, validateConsumerProfile

@app.route("/admin/post/news", methods=['GET', 'POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def manageNews():
  

    return render_template('manage_news.html')


@app.route("/admin/update/news", methods=['GET', 'POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def updateNews():
  

    return render_template('manage_news.html')


@app.route("/admin/delete/news", methods=['GET', 'POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def deleteNews():
  

    return render_template('manage_news.html')

