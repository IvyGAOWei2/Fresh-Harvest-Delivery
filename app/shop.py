from app import app
from flask import render_template, request, session
from math import ceil

from dbFile.config import fetchAll, fetchOne, insertSQL, updateSQL
from common import fakeReview, roleRequired


def discountedProducts(is_full=None):
    sql = """
        SELECT
            p.product_id, p.name, p.description, p.price, pi.image, p.discount_price, p.depot_id, u.unit_name
        FROM 
            Products p
        INNER JOIN 
            DiscountedProducts dp ON p.product_id = dp.product_id
        INNER JOIN
            Discounts d ON dp.discount_id = d.discount_id
        LEFT JOIN 
            ProductImages pi ON p.product_id = pi.product_id AND pi.is_primary = TRUE
        INNER JOIN 
            Unit u ON p.unit_id = u.unit_id
        WHERE 
            d.status = 1 AND p.is_active = TRUE AND p.discount_end_date >= CURDATE()
    """

    if is_full:
        sql += f"ORDER BY d.start_date DESC"
    else:
        sql += f"ORDER BY RAND() LIMIT 4;"
    
    return fetchAll(sql, None, True)

def ordinaryProducts(category=None, page_offset=None):
    sql = """
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
        LEFT JOIN Boxes b ON p.product_id = b.product_id
        LEFT JOIN Packages pkg ON b.package_id = pkg.package_id
        WHERE p.is_active = TRUE 
        AND pi.is_deleted = FALSE 
        AND (pkg.end_date IS NULL OR pkg.end_date >= CURDATE())
    """
    if category:
        sql += f"AND c.category_name = '{category}'"

    sql += " ORDER BY p.product_id ASC LIMIT 9 OFFSET " + page_offset

    return fetchAll(sql, None, True)
def categoriesByCount():
    return fetchAll("SELECT c.category_name, COUNT(p.product_id) AS item_count FROM Category c LEFT JOIN Products p ON c.category_id = p.category_id GROUP BY c.category_name;", None, True)

@app.route("/shop")
def shop():
    page = request.args.get('page')
    category = request.args.get('category')

    if page:
        page_offset = (int(page) - 1) * 9
        current_page = int(page)
    else:
        page_offset = 0
        current_page = 1
    
    sql_total_products = """
        SELECT COUNT(*) AS total_products 
        FROM Products p 
        JOIN Category c ON p.category_id = c.category_id 
        JOIN Unit u ON p.unit_id = u.unit_id 
        JOIN ProductImages pi ON p.product_id = pi.product_id
        LEFT JOIN Boxes b ON p.product_id = b.product_id
        LEFT JOIN Packages pkg ON b.package_id = pkg.package_id
        WHERE p.is_active = TRUE
        AND pi.is_deleted = FALSE
        AND (pkg.end_date IS NULL OR pkg.end_date >= CURDATE())
    """
    if category:
        sql_total_products += f" AND c.category_name = '{category}'"

    total_products = fetchOne(sql_total_products, ())
    total_pages = ceil(total_products[0] / 9)

    products = ordinaryProducts(category, str(page_offset))

    return render_template('shop.html', category=category, categories=categoriesByCount(), products=products, current_page=current_page, total_pages=total_pages, discounted_items=discountedProducts())


@app.route('/product/detail/<int:product_id>')
def shopDetail(product_id):
    sql_product = """
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

    product = fetchOne(sql_product, (product_id,), True)

    if product:
        discounted_price = round(product['price'] * (1 - product['discount_rate'] / 100), 2) if 'discount_rate' in product and product['discount_rate'] else None
        product['discounted_price'] = discounted_price

        # Fetch box items only for active packages
        # boxitems_query = """
        #     SELECT B.box_type, BI.quantity, P.name AS product_name
        #     FROM BoxItems BI
        #     JOIN Boxes B ON BI.box_id = B.box_id
        #     JOIN Products P ON BI.product_id = P.product_id
            JOIN Packages PKG ON B.package_id = PKG.package_id
        #     WHERE B.product_id = %s
            AND PKG.end_date >= CURDATE()
        # """
        # boxitems = fetchAll(boxitems_query, (product_id,), True)

        categories = categoriesByCount()
        discounted_products = discountedProducts()

        for dp in discounted_products:
            dp['discounted_price'] = round(dp['price'] * (1 - dp['discount_rate'] / 100), 2) if 'discount_rate' in dp and dp['discount_rate'] else None

        related_products = ordinaryProducts(app.category_list[product['category_id'] - 1]['category_name'], '0')

        depot_id = session.get('depot_id', 1 if 'depot_id' not in session or session['depot_id'] == 6 else session['depot_id'])

        reviews = fetchAll("SELECT R.rating, DATE_FORMAT(R.review_date, '%b %d, %Y') AS review_date, R.review_text, C.given_name, C.image FROM Reviews R \
            JOIN Consumer C ON R.user_id = C.user_id WHERE R.depot_id = %s AND R.product_id = %s;", \
            (depot_id, product_id), True)

        fake_review = fakeReview()
        for i in range(len(reviews)):
            fake_review.pop()

        is_reviewed = fetchOne("SELECT review_id FROM Reviews WHERE user_id = %s AND depot_id = %s AND product_id = %s;", (session['id'], depot_id, product_id)) if 'id' in session else False

        # return render_template('shop-detail.html', product=product, categories=categories, depotList=app.depot_list, \
        #     categoryList=app.category_list, reviews=reviews, fakeReview=fake_review, is_reviewed=is_reviewed, \
        #     discounted_items=discounted_products, boxitems=boxitems, relatedProducts=related_products)
        return render_template('shop-detail.html', product=product, categories=categories, depotList=app.depot_list, \
            categoryList=app.category_list, reviews=reviews, fakeReview=fake_review, is_reviewed=is_reviewed, \
            discounted_items=discounted_products, relatedProducts=related_products)
    else:
        return render_template('404.html')


@app.route('/product/review', methods=['POST'])
@roleRequired(['Consumer'])
def productReview():
    data = request.form.to_dict()

    try:
        user_id = fetchOne('SELECT user_id FROM Orders WHERE product_id = %s', (data['product_id'],), True)
        update_successful = updateSQL("UPDATE Reviews SET rating = %s, review_text = %s WHERE user_id = %s AND product_id = %s AND depot_id = %s;", \
        (data['rating'], data['review_text'], session['id'], data['product_id'], session['depot_id']))
    except Exception as e:
        update_successful = insertSQL("INSERT INTO Reviews (user_id, depot_id, product_id, rating, review_text) VALUES (%s, %s, %s, %s, %s);", \
        (session['id'], session['depot_id'], data['product_id'], data['rating'], data['review_text']))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500


@app.route("/product/discounted")
def productDiscounted():
    all_discounted = discountedProducts(True)
    return render_template('shop.html', allDiscounted=all_discounted, category=None, categories=categoriesByCount(), total_pages=1, current_page=1)
