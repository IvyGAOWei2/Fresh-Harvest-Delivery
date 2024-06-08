from app import app
from flask import render_template, request, session
from math import ceil

from dbFile.config import fetchAll, fetchOne, insertSQL, updateSQL
from common import fakeReview, roleRequired

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
        SELECT p.product_id, p.name, p.description, p.price, p.stock, 
        CASE 
            WHEN p.discount_end_date < CURDATE() THEN NULL 
            ELSE p.discount_price 
        END AS discount_price, 
        c.category_name, u.unit_name, pi.image
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

    sql_discounted_products = """
            SELECT 
                p.product_id, p.name, p.price, pi.image, d.discount_rate
            FROM 
                Products p
            INNER JOIN 
                DiscountedProducts dp ON p.product_id = dp.product_id
            INNER JOIN 
                Discounts d ON dp.discount_id = d.discount_id
            LEFT JOIN 
                ProductImages pi ON p.product_id = pi.product_id AND pi.is_primary = TRUE
            WHERE 
                d.status = 1 AND p.is_active = TRUE AND p.discount_end_date >= CURDATE()
        """

    # sql_discounted_products += f"ORDER BY d.start_date DESC"
    sql_discounted_products += f"ORDER BY RAND() LIMIT 4;"
    discounted_products = fetchAll(sql_discounted_products, [])

    discounted_items = [
            {
                'product_id': product[0],
                'name': product[1],
                'price': product[2],
                'discount_price': round(product[2] * (1 - product[4] / 100), 2),  # Calculate discounted price
                'image': product[3] or 'image_coming_soon.jpg',  # Fallback image if no image found
                'discount_rate': product[4]
            }
            for product in discounted_products
        ]

    return render_template('shop.html', category=category, categories=categories, products=products, current_page=current_page, total_pages=total_pages, discounted_items=discounted_items)


@app.route('/product/detail/<int:product_id>')
def shopDetail(product_id):
    sql_products = """
        SELECT p.product_id, p.name, p.description, p.price, p.stock, p.depot_id, p.category_id, 
        CASE 
            WHEN p.discount_end_date < CURDATE() THEN NULL 
            ELSE p.discount_price 
        END AS discount_price, 
         u.unit_name, u.unit_std, u.unit_min, pi.image
        FROM Products p 
        JOIN Unit u ON p.unit_id = u.unit_id 
        JOIN ProductImages pi ON p.product_id = pi.product_id 
        WHERE p.is_active = TRUE 
        AND p.product_id = %s 
    """

    product = fetchOne(sql_products, (product_id,), True)

    reviews = fetchAll("SELECT R.rating, DATE_FORMAT(R.review_date, '%b %d, %Y') AS review_date, R.review_text, C.given_name, C.image FROM Reviews R \
        JOIN Consumer C ON R.user_id = C.user_id WHERE R.depot_id = %s AND R.product_id = %s;", \
        (session['depot_id'], product_id), True)

    fake_review = fakeReview()
    for i in range(len(reviews)):
        fake_review.pop()

    categories = fetchAll("SELECT c.category_name, COUNT(p.product_id) AS item_count FROM Category c LEFT JOIN Products p ON c.category_id = p.category_id GROUP BY c.category_name;", None, True)

    is_reviewed = fetchOne("SELECT review_id FROM Reviews WHERE user_id = %s AND depot_id = %s AND product_id = %s;", \
        (session['id'], session['depot_id'], product_id))
    
    return render_template('shop-detail.html', product=product, categories=categories, depotList=app.depot_list, \
        categoryList=app.category_list, reviews=reviews, fakeReview=fake_review, is_reviewed=is_reviewed)


@app.route('/product/review', methods=['POST'])
@roleRequired(['Consumer'])
def productReview():
    data = request.form.to_dict()

    try:
        user_id = fetchOne('SELECT user_id FROM Orders WHERE product_id = %s', (data['product_id'],),True)
        update_successful = updateSQL("UPDATE Reviews SET rating = %s, review_text = %s WHERE user_id = %s AND product_id = %s AND depot_id = %s;", \
        (data['rating'], data['review_text'], session['id'], data['product_id'],session['depot_id']))
    except Exception as e:
        # print(e)
        update_successful = insertSQL("INSERT INTO Reviews (user_id, depot_id, product_id, rating, review_text) VALUES (%s, %s, %s, %s, %s);", \
        (session['id'], session['depot_id'], data['product_id'], data['rating'],data['review_text']))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500