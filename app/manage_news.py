from app import app, shop
from flask import render_template, request, session

# User-defined function
from dbFile.config import fetchOne, insertSQL, updateSQL, fetchAll
from common import roleRequired, validateEmail, validateRegisterEmployee, validateEmployeeProfile, validateConsumerProfile

@app.route("/admin/news", methods=['GET', 'POST'])
@roleRequired(['Local_Manager', 'National_Manager'])
def manageNews():
  

    return render_template('manage_news.html')


@app.route("/consumer/news/detail", methods=['GET', 'POST'])
@roleRequired(['Consumer'])
def newsDetail():
    shop()
    pass
    return render_template('news_detail.html')