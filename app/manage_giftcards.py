from app import app
from flask import render_template, request
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile

@app.route("/giftcards/list", methods = ["GET"])
@roleRequired(['National_Manager'])
def manageGiftcard():
  
    return render_template('manage-giftcards.html')


@app.route("/Giftcard/add",methods = ["POST"])
@roleRequired(['National_Manager'])
def addGiftcard():
    return render_template('manage-giftcards.html')
