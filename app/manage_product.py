from app import app
from flask import render_template, request
from dbFile.config import fetchAll, updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile

@app.route("/product/list", methods = ["GET"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageProduct():
    sql_products = """
        SELECT 
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            p.category_id,
            p.unit_id,
            p.depot_id,
            PI.image AS image
        FROM 
            Products p
        INNER JOIN 
            Category c ON p.category_id = c.category_id
        INNER JOIN 
            Unit u ON p.unit_id = u.unit_id
        INNER JOIN 
            Depots d ON p.depot_id = d.depot_id
        INNER JOIN 
            ProductImages PI ON p.product_id = PI.product_id;
    """
    product_list = fetchAll(sql_products, None, True)
    category_list = fetchAll("""SELECT * FROM Category;""", None, True)
    unit_list = fetchAll("""SELECT * FROM Unit;""", None, True)
    depot_list = fetchAll("""SELECT * FROM Depots;""", None, True)
    return render_template('manage-products.html', productList = product_list, categoryList=category_list, unitList=unit_list, depotList=depot_list)


@app.route("/product/add",methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def addProduct():
    data = dict(request.form)

    product_id = insertSQL("INSERT INTO Products (name, category_id, unit_id, depot_id, price, stock, description) VALUES (%s, %s, %s, %s, %s, %s, %s);", \
        (data['name'], data['category_id'], data['unit_id'], data['depot_id'], data['price'],data['stock'], data['description']))

    img_id = insertSQL("INSERT INTO ProductImages (product_id, image, is_primary, is_deleted) VALUES (%s, %s, %s, %s);", (product_id, 'image_coming_soon.jpg', True, False))
    if product_id:
        return {"status": True}, 200
    else:
        return {"status": False}, 500


@app.route("/product/update", methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def updateProduct():
    verified_data = validateProductProfile(request.form.to_dict())

    product_id = verified_data['product_id']
    verified_data.pop('product_id')

    if verified_data:
        updates,params = [], []
        for key, value in verified_data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(product_id)

    update_successful = updateSQL("UPDATE Products SET " + ", ".join(updates) + " WHERE product_id = %s", params)
    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500

@app.route("/product/delist", methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def productDelist():
    data = request.get_json()

    update_successful = updateSQL("UPDATE Products SET is_active = FALSE WHERE product_id = %s;", (data['product_id'],))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500