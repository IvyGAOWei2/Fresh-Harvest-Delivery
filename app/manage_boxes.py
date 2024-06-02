from jinja2 import TemplateNotFound
from app import app
from flask import render_template, request, session,jsonify
from dbFile.config import fetchAll, fetchOne, updateSQL, insertSQL
from common import roleRequired
from datetime import datetime
from decimal import Decimal
@app.route('/employee/weekly-boxes')
@roleRequired(['Local_Manager', 'National_Manager'])
def manageWeeklyBoxes():
    try:
        user_role = session['type']
        depot_id = session.get('depot_id')
        
        if user_role == 'National_Manager':
            sql_packages = """
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name
                FROM Packages p
                JOIN Depots d ON p.depot_id = d.depot_id
                ORDER BY p.start_date DESC
            """
            packages = fetchAll(sql_packages)
        else:
            sql_packages = """
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name
                FROM Packages p
                JOIN Depots d ON p.depot_id = d.depot_id
                WHERE p.depot_id = %s
                ORDER BY p.start_date DESC
            """
            packages = fetchAll(sql_packages, (depot_id,))
        
        formatted_packages = [
            {
                'package_id': package[0],
                'title': package[1],
                'start_date': package[2].strftime('%d/%m/%Y'),
                'end_date': package[3].strftime('%d/%m/%Y'),
                'depot_name': package[4]
            }
            for package in packages
        ]

        sql_depots = "SELECT depot_id, location FROM Depots"
        depots = fetchAll(sql_depots)
        
        return render_template('boxes.html', user_role=user_role, packageList=formatted_packages, depots=depots)
    except Exception as err:
        
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/api/packages', methods=['GET'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def get_packages_by_depot():
    try:
        user_role = session['type']
        depot_id = request.args.get('depot_id')  # Get the depot_id from query parameters
        
        if user_role == 'National_Manager':
            sql_packages = """
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name
                FROM Packages p
                JOIN Depots d ON p.depot_id = d.depot_id
                {}
                ORDER BY p.start_date DESC
            """
            if depot_id:
                sql_packages = sql_packages.format("WHERE p.depot_id = %s")
                packages = fetchAll(sql_packages, (depot_id,))
            else:
                sql_packages = sql_packages.format("")
                packages = fetchAll(sql_packages)
        else:
            sql_packages = """
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name
                FROM Packages p
                JOIN Depots d ON p.depot_id = d.depot_id
                WHERE p.depot_id = %s
                ORDER BY p.start_date DESC
            """
            packages = fetchAll(sql_packages, (depot_id,))
        
        formatted_packages = [
            {
                'package_id': package[0],
                'title': package[1],
                'start_date': package[2].strftime('%d/%m/%Y'),
                'end_date': package[3].strftime('%d/%m/%Y'),
                'depot_name': package[4]
            }
            for package in packages
        ]
        return jsonify({'packages': formatted_packages})
    except Exception as err:
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500




@app.route('/employee/add-package', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def addPackage():
    try:
        data = request.json
        title = data.get('title')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        user_role = session['type']

        if user_role == 'National_Manager':
            depot_id = data.get('depot_id')
        else:
            depot_id = session['depot_id']

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


@app.route('/employee/package/<int:package_id>')
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
        boxes = {box_type: {'box_id': None, 'price': 0.00, 'products': []} for box_type in box_types}
        
        for box in existing_boxes:
            box_id, box_type, price = box
            boxes[box_type] = {'box_id': box_id, 'price': price, 'products': []}

            # Fetch products for each box
            sql_products = """
                SELECT bi.product_id, p.name, bi.quantity
                FROM BoxItems bi
                JOIN Products p ON bi.product_id = p.product_id
                WHERE bi.box_id = %s
            """
            products = fetchAll(sql_products, (box_id,))
            boxes[box_type]['products'] = [{'id': product[0], 'name': product[1], 'quantity': product[2]} for product in products]

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

        formatted_categories = [{'id': category[0], 'name': category[1]} for category in categories]

        return render_template('manage-box-products.html', package=package_data, boxes=boxes, categories=formatted_categories)
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

@app.route('/employee/add-box-product', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def add_box_product():
    try:
        data = request.json
        box_id = data.get('box_id')
        product_id = data.get('product_id')
        quantity = int(data.get('quantity'))

        if not all([box_id, product_id, quantity]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        if product_id == 'undefined':
            return jsonify({'status': False, 'message': 'Invalid product selection'}), 400

        # Insert product into the Small box
        sql_insert_box_item = """
            INSERT INTO BoxItems (box_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """
        insertSQL(sql_insert_box_item, (box_id, product_id, quantity))

        # Automatically add the product to Medium and Large boxes
        sql_get_box_ids = "SELECT box_id, box_type FROM Boxes WHERE package_id = (SELECT package_id FROM Boxes WHERE box_id = %s)"
        boxes = fetchAll(sql_get_box_ids, (box_id,))
        for box in boxes:
            if box[1] == 'Medium':
                medium_quantity =  quantity + 1
                insertSQL(sql_insert_box_item, (box[0], product_id, medium_quantity))
            elif box[1] == 'Large':
                large_quantity = quantity + 2
                insertSQL(sql_insert_box_item, (box[0], product_id, large_quantity))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/employee/update-box-product', methods=['POST'])
def update_box_product():
    try:
        data = request.json
        box_id = data.get('box_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not all([box_id, product_id, quantity]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        # Ensure quantity is a valid integer
        try:
            quantity = int(quantity)
        except ValueError:
            return jsonify({'status': False, 'message': 'Invalid quantity value'}), 400

        if quantity == 0:
            sql_delete_product = "DELETE FROM BoxItems WHERE box_id = %s AND product_id = %s"
            updateSQL(sql_delete_product, (box_id, product_id))
        else:
            sql_update_product = """
                UPDATE BoxItems
                SET quantity = %s
                WHERE box_id = %s AND product_id = %s
            """
            updateSQL(sql_update_product, (quantity, box_id, product_id))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500