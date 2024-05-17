from app import app
from flask import render_template, request
from math import ceil

from dbFile.config import fetchAll, fetchOne
from common import fakeReview

@app.route("/shop")
def shop():
    page = request.args.get('page')
    category = request.args.get('category')
    # print(category)
    if page:
        page_offset = (int(page) - 1) * 9
        current_page = int(page)
    else:
        page_offset = 0
        current_page = 1

    categories = fetchAll("SELECT c.category_name, COUNT(p.product_id) AS item_count FROM Category c LEFT JOIN  Products p ON c.category_id = p.category_id GROUP BY c.category_name;", None, True)
    
    sql_total_products = """
        SELECT COUNT(*) AS total_products 
        FROM Products p 
        JOIN Category c ON p.category_id = c.category_id 
        JOIN Unit u ON p.unit_id = u.unit_id 
        JOIN ProductImages pi ON p.product_id = pi.product_id
        WHERE p.is_active = TRUE
        AND pi.is_deleted = FALSE
    """
    if category:
        sql_total_products += f" AND c.category_name = '{category}'"

    total_products = fetchOne(sql_total_products, ())
    total_pages = ceil(total_products[0]/9)

    sql_products = """
        SELECT p.product_id, p.name, p.description, p.price, p.discount_price, p.stock, c.category_name, u.unit_name, pi.image 
        FROM Products p 
        JOIN Category c ON p.category_id = c.category_id 
        JOIN Unit u ON p.unit_id = u.unit_id 
        JOIN ProductImages pi ON p.product_id = pi.product_id 
        WHERE p.is_active = TRUE 
        AND pi.is_deleted = FALSE 
    """
    if category:
        sql_products += f"AND c.category_name = '{category}'"

    sql_products += "ORDER BY p.product_id ASC LIMIT 9 OFFSET " + str(page_offset)

    products = fetchAll(sql_products, None, True)

    return render_template('shop.html', category=category, categories=categories, products=products, current_page=current_page, total_pages=total_pages)

@app.route('/product/detail')
def shopDetail():
    try:
        product_id = int(request.args.get('product_id'))

        product = fetchOne("SELECT P.product_id,P.name,P.description,P.price,P.discount_price,P.stock,C.category_name,U.unit_name,D.location AS depot_location,PI.image AS primary_image \
            FROM Products AS P \
            LEFT JOIN Category AS C ON P.category_id = C.category_id \
            LEFT JOIN Unit AS U ON P.unit_id = U.unit_id \
            LEFT JOIN Depots AS D ON P.depot_id = D.depot_id \
            LEFT JOIN (SELECT * FROM ProductImages WHERE is_deleted = FALSE AND is_primary = TRUE) AS PI ON P.product_id = PI.product_id \
            WHERE P.product_id = %s;", (product_id,), True)

        categories = fetchAll("SELECT c.category_name, COUNT(p.product_id) AS item_count FROM Category c LEFT JOIN  Products p ON c.category_id = p.category_id GROUP BY c.category_name;", None, True)

        return render_template('shop-detail.html', product=product, categories=categories, reviews=fakeReview())
    except:
        return render_template('404.html')

