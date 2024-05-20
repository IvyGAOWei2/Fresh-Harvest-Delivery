from app import app
from flask import render_template, request, session,jsonify
from dbFile.config import fetchAll, fetchOne, updateSQL, insertSQL
from common import roleRequired, getUserProfile, validateEmployeeProfile
from datetime import datetime
from decimal import Decimal



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
    return render_template('manage-products.html', productList = product_list)

@app.route('/employee/discounts')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageDiscount():
    try:
        now = datetime.now().date()

        # Update the status of expired discounts
        sql_update_expired = """
            UPDATE Discounts
            SET status = FALSE
            WHERE end_date < %s
        """
        updateSQL(sql_update_expired, (now,))

        # Fetch the latest discounts
        sql_discounts = """
            SELECT
                discount_id,
                title,
                description,
                start_date,
                end_date,
                discount_rate,
                status
            FROM
                Discounts
            ORDER BY
                start_date DESC
        """
        discount_list = fetchAll(sql_discounts)
        return render_template('discounts.html', discountList=discount_list, now=now)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/employee/add-discount', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def add_discount():
    try:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        discount_rate = data.get('discount_rate')
        
        if not all([title, description, start_date, end_date, discount_rate]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400
        
        sql_insert_discount = """
            INSERT INTO Discounts (title, description, start_date, end_date, discount_rate)
            VALUES (%s, %s, %s, %s, %s)
        """
        discount_id = insertSQL(sql_insert_discount, (title, description, start_date, end_date, discount_rate))
        
        if discount_id:
            return jsonify({'status': True})
        else:
            return jsonify({'status': False, 'message': 'Failed to add discount'}), 500
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/employee/update-discount/<int:discount_id>', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def update_discount(discount_id):
    try:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        discount_rate = data.get('discountRate')
        end_date = data.get('endDate')

        if not title or not description or not discount_rate or not end_date:
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_update_discount = """
            UPDATE Discounts
            SET title = %s, description = %s, discount_rate = %s, end_date = %s
            WHERE discount_id = %s
        """
        updateSQL(sql_update_discount, (title, description, discount_rate, end_date, discount_id))

        return jsonify({'status': True})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/employee/manage-discount-products/<int:discount_id>')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageDiscountProducts(discount_id):
    try:
        sql_discounted_products = """
            SELECT 
                dp.id,
                p.name,
                p.description,
                p.price,
                dp.discount_price,
                c.category_name,
                d.discount_rate
            FROM 
                DiscountedProducts dp
            INNER JOIN 
                Products p ON dp.product_id = p.product_id
            INNER JOIN 
                Category c ON p.category_id = c.category_id
            INNER JOIN 
                Discounts d ON dp.discount_id = d.discount_id
            WHERE 
                dp.discount_id = %s
        """
        discounted_product_list = fetchAll(sql_discounted_products, (discount_id,))
        discount_rate = fetchOne("SELECT discount_rate FROM Discounts WHERE discount_id = %s", (discount_id,), withDescription=True)['discount_rate']
        return render_template('manage-discount-products.html', discountedProductList=discounted_product_list, discount_id=discount_id, discountRate=discount_rate)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/employee/add-discount-product', methods=['POST'])
def add_discount_product():
    try:
        data = request.json
        discount_id = data.get('discount_id')
        product_id = data.get('product_id')

        if not discount_id or not product_id:
            return jsonify({'status': False, 'message': 'Discount ID and Product ID are required'}), 400

        # Fetch discount rate
        sql_discount_rate = "SELECT discount_rate FROM Discounts WHERE discount_id = %s"
        discount_rate = fetchOne(sql_discount_rate, (discount_id,))
        print(f"Fetched discount_rate: {discount_rate}")

        # Fetch product price
        sql_product_price = "SELECT price FROM Products WHERE product_id = %s"
        product_price = fetchOne(sql_product_price, (product_id,))
        print(f"Fetched product_price: {product_price}")

        if not discount_rate or not product_price:
            return jsonify({'status': False, 'message': 'Invalid discount or product ID'}), 400

        # Calculate discount price
        discount_price = product_price['price'] * (1 - discount_rate[0] / Decimal('100'))
        print(f"Calculated discount_price: {discount_price}")

        # Insert discounted product
        sql_insert_discounted_product = """
            INSERT INTO DiscountedProducts (discount_id, product_id, discount_price)
            VALUES (%s, %s, %s)
        """
        row_count = insertSQL(sql_insert_discounted_product, (discount_id, product_id, discount_price))
        print(f"Insert row_count: {row_count}")

        if row_count > 0:
            return jsonify({'status': True, 'message': 'Discounted product added successfully'})
        else:
            return jsonify({'status': False, 'message': 'Failed to add discounted product'}), 500
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        sql = "SELECT category_id as id, category_name as name FROM Category"
        categories = fetchAll(sql, withDescription=True)
        return jsonify({'categories': categories})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('category_id')
        sql = "SELECT product_id as id, name FROM Products"
        if category_id:
            sql += " WHERE category_id = %s"
            products = fetchAll(sql, (category_id,), withDescription=True)
        else:
            products = fetchAll(sql, withDescription=True)
        return jsonify({'products': products})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/api/discounts', methods=['GET'])
def get_discounts():
    try:
        sql_discounts = "SELECT discount_id as id, title, discount_rate FROM Discounts"
        discounts = fetchAll(sql_discounts, withDescription=True)
        return jsonify({'discounts': discounts})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/test-insert', methods=['GET'])
def test_insert():
    try:
        sql_insert_test = "INSERT INTO DiscountedProducts (discount_id, product_id, discount_price) VALUES (%s, %s, %s)"
        test_discount_id = 1
        test_product_id = 2
        test_discount_price = 3.99
        row_count = insertSQL(sql_insert_test, (test_discount_id, test_product_id, test_discount_price))
        print(f"Test Insert row_count: {row_count}")
        if row_count > 0:
            return "Test insert successful", 200
        else:
            return "Test insert failed", 500
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database error occurred", 500
