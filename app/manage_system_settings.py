from app import app
from flask import render_template, request
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, newShipping

@app.route("/system/setting", methods = ["GET"])
@roleRequired(['National_Manager'])
def manageSettings():
    return render_template('manage-system-settings.html', shipping=app.shipping, categories = app.category_list, units = app.unit_list)


@app.route('/shipping/update', methods=['POST'])
def updateShipping():
    shipping = request.form.get("shipping")
    if newShipping(shipping):
        app.shipping = int(shipping)
        return {"status": True}, 200
    else:
        return {"status": False}, 500

@app.route('/units/update', methods=['POST'])
def updateUnits():
    data =  request.form.to_dict()
    try:
        updateSQL("UPDATE Unit SET unit_name = %s, unit_std = %s, unit_min = %s WHERE unit_id = %s;", \
        (data['unit_name'], data['unit_std'], data['unit_min'], data['unit_id']))
    except:
        return {"status": False}, 500
    else:
        app.unit_list = fetchAll("""SELECT * FROM Unit;""", None, True)
        return {"status": True}, 200

@app.route('/units/add', methods=['POST'])
def addUnits():
    data = request.form.to_dict()
    try:
        insertSQL("INSERT INTO Unit (unit_name, unit_std, unit_min) VALUES (%s,%s,%s);", \
        (data['unit_name'],data['unit_std'],data['unit_min']))
    except:
        return {"status": False}, 500
    else:
        app.unit_list = fetchAll("""SELECT * FROM Unit;""", None, True)
        return {"status": True}, 200

@app.route('/category/add', methods=['POST'])
def addCategories():
    data = request.form.to_dict()
    try:
        insertSQL("INSERT INTO Category (category_name) VALUES (%s);", (data['category_name'],))
    except:
        return {"status": False}, 500
    else:
        app.category_list = fetchAll("""SELECT * FROM Category;""", None, True)
        return {"status": True}, 200


@app.route('/category/update', methods=['POST'])
def updateCategories():
    data =  request.form.to_dict()
    try:
        updateSQL("UPDATE Category SET category_name = %s WHERE category_id = %s;", (data['category_name'], data['category_id']))
    except:
        return {"status": False}, 500
    else:
        app.category_list = fetchAll("""SELECT * FROM Category;""", None, True)
        return {"status": True}, 200







