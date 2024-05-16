from app import app
from flask import render_template, request, session
from dbFile.config import fetchAll, fetchOne,updateSQL

# User-defined function
from dbFile.config import updateSQL
from common import roleRequired, getUserProfile, validateEmployeeProfile

@app.route("/employee/products")
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
    # print(product_list)
    return render_template('manage-products.html', productList = product_list)