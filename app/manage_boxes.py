from jinja2 import TemplateNotFound
from app import app
from flask import render_template, request, session,jsonify
from dbFile.config import fetchAll, fetchOne, updateSQL, insertSQL
from common import roleRequired
from datetime import datetime
from decimal import Decimal
@app.route('/employee/weekly-boxes')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageWeeklyBoxes():
    try:
        sql_packages = """
            SELECT package_id, title, start_date, end_date, depot_id
            FROM Packages
            ORDER BY start_date DESC
        """
        packages = fetchAll(sql_packages)
        
        formatted_packages = [
            {
                'package_id': package[0],
                'title': package[1],
                'start_date': package[2],
                'end_date': package[3],
                'depot_id': package[4]
            }
            for package in packages
        ]

        return render_template('weekly_boxes.html', packageList=formatted_packages)
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/add-package', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def addPackage():
    try:
        data = request.json
        title = data.get('title')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        depot_id = data.get('depot_id')

        if not all([title, start_date, end_date, depot_id]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_insert_package = """
            INSERT INTO Packages (title, start_date, end_date, depot_id)
            VALUES (%s, %s, %s, %s)
        """
        package_id = insertSQL(sql_insert_package, (title, start_date, end_date, depot_id))

        return jsonify({'status': True, 'package_id': package_id})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': f'Database error occurred: {err}'}), 500



@app.route('/employee/box-products/<int:package_id>')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manage_box_products(package_id):
    try:
        sql_package = "SELECT title, start_date, end_date FROM Packages WHERE package_id = %s"
        package = fetchOne(sql_package, (package_id,))
        
        if not package:
            return "Package not found", 404

        sql_boxes = "SELECT box_id, box_type, price FROM Boxes WHERE package_id = %s"
        existing_boxes = fetchAll(sql_boxes, (package_id,))
        
        # Ensure Small, Medium, and Large boxes exist
        box_types = ['Small', 'Medium', 'Large']
        boxes = {box_type: {'box_id': None, 'price': 0.00} for box_type in box_types}
        
        for box in existing_boxes:
            boxes[box[1]] = {'box_id': box[0], 'price': box[2]}
        
        # Create any missing boxes with default values
        for box_type in box_types:
            if boxes[box_type]['box_id'] is None:
                sql_insert_box = """
                    INSERT INTO Boxes (package_id, box_type, price)
                    VALUES (%s, %s, %s)
                """
                box_id = insertSQL(sql_insert_box, (package_id, box_type, 0.00))
                boxes[box_type]['box_id'] = box_id

        sql_categories = "SELECT category_id, category_name FROM Category"
        categories = fetchAll(sql_categories)

        package_data = {
            'package_id': package_id,
            'title': package[0],
            'start_date': package[1],
            'end_date': package[2]
        }

        return render_template('box_products.html', package=package_data, boxes=boxes, categories=categories)
    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500



@app.route('/employee/update-box-price', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def update_box_price():
    try:
        data = request.json
        box_id = data.get('box_id')
        price = data.get('price')

        if not all([box_id, price]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_update_price = """
            UPDATE Boxes
            SET price = %s
            WHERE box_id = %s
        """
        updateSQL(sql_update_price, (price, box_id))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500
@app.route('/api/products', methods=['GET'])
def get_products_by_category():
    category_id = request.args.get('category_id')
    try:
        sql_products = "SELECT product_id, name FROM Products WHERE category_id = %s"
        products = fetchAll(sql_products, (category_id,))
        return jsonify({'products': products})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500
@app.route('/api/categories', methods=['GET'])
def get_all_categories():
    try:
        # Fetch categories from the database
        sql_categories = "SELECT category_id, category_name FROM Category"
        categories = fetchAll(sql_categories)
        
        # Log the fetched raw categories
        print("Raw fetched categories:", categories)
        
        # Convert list of tuples to list of dictionaries
        categories_list = [{'category_id': category[0], 'category_name': category[1]} for category in categories]
        
        # Log the converted categories
        print("Converted categories:", categories_list)
        
        # Return the list of dictionaries as a JSON response
        return jsonify({'categories': categories_list})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/employee/add-box-product', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def add_box_product():
    try:
        data = request.json
        box_id = data.get('box_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not all([box_id, product_id, quantity]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_insert_box_item = """
            INSERT INTO BoxItems (box_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """
        insertSQL(sql_insert_box_item, (box_id, product_id, quantity))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500
