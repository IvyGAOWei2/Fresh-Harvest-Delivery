from app import app
from flask import render_template, request, redirect,url_for
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile

@app.route("/system/setting", methods = ["GET"])
@roleRequired(['National_Manager'])
def manageSettings():
    
    return render_template('manage-system-settings.html', categories = app.category_list, units = app.unit_list)


@app.route('/shipping/update', methods=['POST'])
def updateShipping():
    # for depot in shipping_prices.keys():
    #     new_price = request.form.get(f'price_{depot}')
    #     if new_price:
    #         shipping_prices[depot] = float(new_price)
    return redirect(url_for('manageSettings'))

@app.route('/units/update', methods=['POST'])
def updateUnits():
    new_unit = request.form.get('new_unit')
    # if new_unit:
    #     units.append(new_unit)
    return redirect(url_for('manageSettings'))

@app.route('/units/add', methods=['POST'])
def addUnits():
    new_unit = request.form.get('new_unit')
    # if new_unit:
    #     units.append(new_unit)
    return redirect(url_for('manageSettings'))


@app.route('/category/add', methods=['POST'])
def addCategories():
    new_category = request.form.get('new_category')
    # if new_category:
    #     categories.append(new_category)
    return redirect(url_for('manageSettings'))

@app.route('/update/categories', methods=['POST'])
def updateCategories():
    new_category = request.form.get('new_category')
    # if new_category:
    #     categories.append(new_category)
    return redirect(url_for('manageSettings'))







