from app import app
from flask import render_template, request, session
from dbFile.config import fetchAll, fetchOne,updateSQL

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, getUserProfile, validateEmployeeProfile

@app.route("/product/list", methods = ["GET","POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageProduct():
    sql_products = """
        SELECT 
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            c.category_name AS category,
            u.unit_name AS unit,
            d.location AS depot,
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
    product_list = fetchAll(sql_products)
    # print(product_list)
    return render_template('manage-products.html', productList = product_list)


@app.route("/product/add",methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def addProduct():
    data = dict(request.form)

    product_id = insertSQL("INSERT INTO Products (name, description, price, stock) VALUES (%s, %s, %s, %s);", \
        (data['name'], data['description'],data['price'], data['stock']))

    if product_id:
        return {"status": True}, 200
    else:
        return {"status": False}, 500


@app.route("/product/update", methods = ["GET","POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def updateProduct():
    print(request.form.to_dict())
    sql_products = """
        SELECT 
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            c.category_name AS category,
            u.unit_name AS unit,
            d.location AS depot
        FROM 
            Products p
        INNER JOIN 
            Category c ON p.category_id = c.category_id
        INNER JOIN 
            Unit u ON p.unit_id = u.unit_id
        INNER JOIN 
            Depots d ON p.depot_id = d.depot_id;
    """
    product_list = fetchAll(sql_products)
    return render_template('manage-products.html', productList = product_list)



@app.route("/product/delist/<int:product_id>", methods = ["GET","POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def delistProduct(product_id):
    sql_products = """
        SELECT 
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            c.category_name AS category,
            u.unit_name AS unit,
            d.location AS depot
        FROM 
            Products p
        INNER JOIN 
            Category c ON p.category_id = c.category_id
        INNER JOIN 
            Unit u ON p.unit_id = u.unit_id
        INNER JOIN 
            Depots d ON p.depot_id = d.depot_id;
    """
    product_list = fetchAll(sql_products)
    return render_template('manage-products.html', productList = product_list, )