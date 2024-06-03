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
        SELECT p.product_id, p.name, p.description, p.price, p.stock, c.category_name, u.unit_name, pi.image        FROM Products p 
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
                d.status = 1 AND p.is_active = TRUE
            ORDER BY 
                d.start_date DESC
        """
    discounted_products = fetchAll(sql_discounted_products, [])

    discounted_items = [
            {
                'product_id': product[0],
                'name': product[1],
                'price': product[2],
                'discount_price': round(product[2] * (1 - product[4] / 100), 2),  # Calculate discounted price
                'image': product[3] or 'default.jpg',  # Fallback image if no image found
                'discount_rate': product[4]
            }
            for product in discounted_products
        ]

    return render_template('shop.html', category=category, categories=categories, products=products, current_page=current_page, total_pages=total_pages, discounted_items=discounted_items)
@app.route('/product/detail')
def shopDetail():
    try:
        product_id = int(request.args.get('product_id'))
       
        sql_query = """
            SELECT 
                P.product_id, P.name, P.description, P.price, P.stock, 
                C.category_name, U.unit_name, D.location AS depot_location, 
                PI.image AS primary_image, COALESCE(DS.discount_rate, 0) AS discount_rate 
            FROM 
                Products AS P 
            LEFT JOIN 
                Category AS C ON P.category_id = C.category_id 
            LEFT JOIN 
                Unit AS U ON P.unit_id = U.unit_id 
            LEFT JOIN 
                Depots AS D ON P.depot_id = D.depot_id 
            LEFT JOIN 
                (SELECT * FROM ProductImages WHERE is_deleted = FALSE AND is_primary = TRUE) AS PI ON P.product_id = PI.product_id 
            LEFT JOIN 
                DiscountedProducts DP ON P.product_id = DP.product_id 
            LEFT JOIN 
                Discounts DS ON DP.discount_id = DS.discount_id AND DS.status = TRUE 
            WHERE 
                P.product_id = %s
        """

        product = fetchOne(sql_query, (product_id,), True)

        if product:
            discounted_price = round(product['price'] * (1 - product['discount_rate'] / 100), 2)
            product['discounted_price'] = discounted_price

            categories = fetchAll("SELECT c.category_name, COUNT(p.product_id) AS item_count FROM Category c LEFT JOIN Products p ON c.category_id = p.category_id GROUP BY c.category_name;", None, True)

            discounted_products = fetchAll("""
                SELECT 
                    P.product_id, P.name, P.description, P.price, P.stock, 
                    C.category_name, U.unit_name, PI.image AS primary_image, 
                    COALESCE(DS.discount_rate, 0) AS discount_rate 
                FROM 
                    Products AS P 
                LEFT JOIN 
                    Category AS C ON P.category_id = C.category_id 
                LEFT JOIN 
                    Unit AS U ON P.unit_id = U.unit_id 
                LEFT JOIN 
                    (SELECT * FROM ProductImages WHERE is_deleted = FALSE AND is_primary = TRUE) AS PI ON P.product_id = PI.product_id 
                LEFT JOIN 
                    DiscountedProducts DP ON P.product_id = DP.product_id 
                LEFT JOIN 
                    Discounts DS ON DP.discount_id = DS.discount_id AND DS.status = TRUE 
                WHERE 
                    DS.status = TRUE
            """, None, True)

            for dp in discounted_products:
                dp['discounted_price'] = round(dp['price'] * (1 - dp['discount_rate'] / 100), 2)

            return render_template('shop-detail.html', product=product, categories=categories, discounted_products=discounted_products, reviews=fakeReview())
        else:
            print("Product not found.")
            return render_template('404.html')
    except Exception as e:
        print(f"Error: {e}")
        return render_template('404.html')