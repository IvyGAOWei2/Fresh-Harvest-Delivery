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
        now = datetime.now().date()
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
        
        
        formatted_discount_list = [
            {
                'discount_id': discount[0],
                'title': discount[1],
                'description': discount[2],
                'start_date': discount[3],
                'end_date': discount[4],
                'discount_rate': str(discount[5]),  # Convert Decimal to string
                'status': 'Active' if discount[6] else 'Inactive'
            }
            for discount in discount_list
        ]

        return render_template('discounts.html', discountList=formatted_discount_list, now=now.strftime('%d/%m/%Y'))
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

        if not all([title, description, start_date, end_date, discount_rate]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        # Log the data being inserted
        print(f"Inserting discount: Title={title}, Description={description}, Start Date={start_date}, End Date={end_date}, Discount Rate={discount_rate}")

        sql_insert_discount = """
            INSERT INTO Discounts (title, description, start_date, end_date, discount_rate)
            VALUES (%s, %s, %s, %s, %s)
        """
        discount_id = insertSQL(sql_insert_discount, (title, description, start_date, end_date, discount_rate))

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
        sql_discount_rate = "SELECT discount_rate FROM Discounts WHERE discount_id = %s"
        discount_rate = fetchOne(sql_discount_rate, (discount_id,))

        sql_discounted_products = """
            SELECT 
                dp.id,
                p.product_id,
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

        return render_template('manage-discount-products.html', discount_id=discount_id, discountedProductList=formatted_product_list, discountRate=str(discount_rate[0]))


    except Exception as e:
        print(f"Error: {e}")
        return render_template('manage-discount-products.html', discountedProductList=[], discountRate=str(discount_rate[0]))
    
@app.route('/employee/add-discount-product', methods=['POST'])
def add_discount_product():
    try:
        data = request.json
        discount_id = data.get('discount_id')
        product_id = data.get('product_id')

        if not discount_id or not product_id:
            return jsonify({'status': False, 'message': 'Discount ID and Product ID are required'}), 400

        # Insert discounted product without discount_price
        sql_insert_discounted_product = """
            INSERT INTO DiscountedProducts (discount_id, product_id)
            VALUES (%s, %s)
        """
        row_count = insertSQL(sql_insert_discounted_product, (discount_id, product_id))

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
        categories = fetchAll("SELECT * FROM Category")
        print("Fetched categories:", categories)
        return jsonify(categories)
    except Exception as e:
        print("Error occurred while fetching categories:", str(e))
        return jsonify({"error": "An error occurred while fetching categories"}), 500

    
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

        return jsonify({'status': True, 'message': 'Product updated successfully'})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500
