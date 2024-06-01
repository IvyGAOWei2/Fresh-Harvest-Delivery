from jinja2 import TemplateNotFound
from app import app
from flask import render_template, request, session,jsonify
from dbFile.config import fetchAll, fetchOne, updateSQL, insertSQL
from common import roleRequired, getUserProfile, validateEmployeeProfile
from datetime import datetime
from decimal import Decimal


@app.route('/api/discounts', methods=['GET'])
def get_discounts():
    try:
        sql_discounts = "SELECT discount_id as id, title, discount_rate FROM Discounts"
        discounts = fetchAll(sql_discounts, withDescription=True)
        return jsonify({'discounts': discounts})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/discounts')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageDiscount():
    try:
        user_role = session['type']
        now = datetime.now().date()
        
        # SQL query based on user role
        sql_discounts = """
            SELECT
                d.discount_id,
                d.title,
                d.description,
                d.start_date,
                d.end_date,
                d.discount_rate,
                d.status,
                dp.location as depot_name,
                d.depot_id
            FROM
                Discounts d
            LEFT JOIN
                Depots dp ON d.depot_id = dp.depot_id
        """
        if user_role != 'National_Manager':
            sql_discounts += " WHERE d.depot_id = %s"
            sql_discounts += " ORDER BY d.start_date DESC"
            discount_list = fetchAll(sql_discounts, (session['depot_id'],))
        else:
            sql_discounts += " ORDER BY d.start_date DESC"
            discount_list = fetchAll(sql_discounts)

        formatted_discount_list = [
            {
                'discount_id': discount[0],
                'title': discount[1],
                'description': discount[2],
                'start_date': discount[3].strftime('%d/%m/%Y'),  # Format date as DD/MM/YYYY
                'end_date': discount[4].strftime('%d/%m/%Y'),  # Format date as DD/MM/YYYY
                'discount_rate': str(discount[5]),  # Convert Decimal to string
                'status': 'Active' if discount[6] else 'Inactive',
                'depot_name': discount[7],
                'depot_id': discount[8]
            }
            for discount in discount_list
        ]

        # Fetch depots
        sql_depots = "SELECT depot_id, location FROM Depots"
        depots = fetchAll(sql_depots)

        return render_template('discounts.html', discountList=formatted_discount_list, depots=depots, user_role=user_role, now=now.strftime('%d/%m/%Y'))
    except Exception as err:
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
        user_role = session['type']

        if user_role == 'National_Manager':
            depot_id = data.get('depot_id')
        else:
            depot_id = session['depot_id']

        if not all([title, description, start_date, end_date, discount_rate, depot_id]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_insert_discount = """
            INSERT INTO Discounts (title, description, start_date, end_date, discount_rate, depot_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        discount_id = insertSQL(sql_insert_discount, (title, description, start_date, end_date, discount_rate, depot_id))

        if discount_id:
            return jsonify({'status': True, 'discount_id': discount_id})
        else:
            return jsonify({'status': False, 'message': 'Failed to add discount'}), 500
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': f'Database error occurred: {err}'}), 500


@app.route('/employee/update-discount/<int:discount_id>', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def update_discount(discount_id):
    try:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        discount_rate = data.get('discount_rate')
        end_date = data.get('end_date')

        if not all([title, description, discount_rate, end_date]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_update_discount = """
            UPDATE Discounts
            SET title = %s, description = %s, discount_rate = %s, end_date = %s
            WHERE discount_id = %s
        """
        updateSQL(sql_update_discount, (title, description, discount_rate, end_date, discount_id))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/deactivate-discount/<int:discount_id>', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def deactivate_discount(discount_id):
    try:
        sql_deactivate_discount = "UPDATE Discounts SET status = FALSE WHERE discount_id = %s"
        updateSQL(sql_deactivate_discount, (discount_id,))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/activate-discount/<int:discount_id>', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def activate_discount(discount_id):
    try:
        sql_activate_discount = "UPDATE Discounts SET status = TRUE WHERE discount_id = %s"
        updateSQL(sql_activate_discount, (discount_id,))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/manage-discount-products/<int:discount_id>')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageDiscountProducts(discount_id):
    try:
        sql_discount_details = "SELECT title, discount_rate, depot_id, start_date, end_date FROM Discounts WHERE discount_id = %s"
        discount_details = fetchOne(sql_discount_details, (discount_id,))
        
        sql_discounted_products = """
            SELECT 
                dp.id,
                p.name,
                p.description,
                p.price,
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
        print(f"Fetched discounted products: {discounted_product_list}")

        formatted_product_list = [
            {
                'id': product[0],
                'product_id': product[1],
                'name': product[2],
                'description': product[3],
                'price': str(product[4]),
                'category_name': product[5],
                'discount_rate': str(product[6]),
            }
            for product in discounted_product_list
        ]
        print(f"Formatted product list: {formatted_product_list}")

        return render_template('manage-discount-products.html',
                               discount_id=discount_id,
                               discountedProductList=formatted_product_list,
                               discount_title=discount_details[0],
                               discount_start=discount_details[3],
                               discount_end=discount_details[4],
                               discountRate=str(discount_details[1]),
                               depot_id=discount_details[2])
    except Exception as e:
        print(f"Error: {e}")
        return render_template('manage-discount-products.html', discountedProductList=[], discountRate='0', depot_id=0)
    
@app.route('/employee/add-discount-product', methods=['POST'])
def add_discount_product():
    try:
        data = request.json
        discount_id = data.get('discount_id')
        product_id = data.get('product_id')

        if not discount_id or not product_id:
            return jsonify({'status': False, 'message': 'Discount ID and Product ID are required'}), 400

        # Fetch depot ID and discount rate from the discount
        sql_discount_details = "SELECT depot_id, discount_rate FROM Discounts WHERE discount_id = %s"
        discount_details = fetchOne(sql_discount_details, (discount_id,))
        if not discount_details:
            return jsonify({'status': False, 'message': 'Discount not found'}), 404

        depot_id, discount_rate = discount_details

        # Check if the product belongs to the same depot
        sql_product_depot = "SELECT depot_id FROM Products WHERE product_id = %s"
        product_depot_id = fetchOne(sql_product_depot, (product_id,))
        if not product_depot_id or product_depot_id[0] != depot_id:
            return jsonify({'status': False, 'message': 'Product does not belong to the same depot'}), 400

        # Insert discounted product with discount_price
        sql_insert_discounted_product = """
            INSERT INTO DiscountedProducts (discount_id, product_id)
            VALUES (%s, %s)
        """
        row_count = insertSQL(sql_insert_discounted_product, (discount_id, product_id))
        print(f"Insert row_count: {row_count}")

        # Update the product's discount price
        sql_update_product = """
            UPDATE Products
            SET discount_price = price - (price * %s / 100)
            WHERE product_id = %s
        """
        updateSQL(sql_update_product, (discount_rate, product_id))

        if row_count > 0:
            return jsonify({'status': True, 'message': 'Discounted product added successfully'})
        else:
            return jsonify({'status': False, 'message': 'Failed to add discounted product'}), 500
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500



@app.route('/api/categories')
def get_categories():
    try:
        print("Attempting to fetch categories from the database.")
        categories = fetchAll("SELECT category_id, category_name FROM Category")
        print("Fetched categories:", categories)
        formatted_categories = [{'id': category[0], 'name': category[1]} for category in categories]
        return jsonify({'categories': formatted_categories})
    except Exception as e:
        print("Error occurred while fetching categories:", str(e))
        return jsonify({"error": "An error occurred while fetching categories"}), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('category_id')
        depot_id = request.args.get('depot_id')
        sql = "SELECT product_id as id, name FROM Products WHERE is_active = TRUE"
        
        params = []
        if category_id:
            sql += " AND category_id = %s"
            params.append(category_id)
        if depot_id:
            sql += " AND depot_id = %s"
            params.append(depot_id)
        
        products = fetchAll(sql, params, withDescription=True)
        return jsonify({'products': products})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/update-discount-product/<int:product_id>', methods=['POST'])
def update_discount_product(product_id):
    try:
        data = request.json
        name = data.get('name')
        category_name = data.get('category_name')
        description = data.get('description')
        price = data.get('price')
        
        if not all([name, category_name, description, price]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_update_product = """
            UPDATE Products
            SET name = %s, description = %s, price = %s
            WHERE product_id = %s
        """
        updateSQL(sql_update_product, (name, description, price, product_id))
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500
@app.route('/api/discounts', methods=['GET'])
def get_discounts():
    try:
        sql_discounts = "SELECT discount_id as id, title, discount_rate FROM Discounts"
        discounts = fetchAll(sql_discounts, withDescription=True)
        return jsonify({'discounts': discounts})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500