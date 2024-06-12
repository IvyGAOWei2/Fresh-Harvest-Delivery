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
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name, p.end_date >= CURRENT_DATE AS is_active
                FROM Packages p
                JOIN Depots d ON p.depot_id = d.depot_id
                ORDER BY p.start_date DESC
            """
            packages = fetchAll(sql_packages)
        else:
            sql_packages = """
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name, p.end_date >= CURRENT_DATE AS is_active
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
                'start_date': package[2].strftime('%Y-%m-%d'),
                'end_date': package[3].strftime('%Y-%m-%d'),
                'depot_name': package[4],
                'is_active': bool(package[5])
            }
            for package in packages
        ]

        sql_depots = "SELECT depot_id, location FROM Depots WHERE location != 'NZ'"
        depots = fetchAll(sql_depots)
        
        return render_template('boxes.html', user_role=user_role, packageList=formatted_packages, depots=depots)
    except Exception as err:
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500


@app.route('/api/packages', methods=['GET'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def get_packages_by_depot():
    try:
        user_role = session['type']
        depot_id = request.args.get('depot_id')
        
        if user_role == 'National_Manager':
            sql_packages = """
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name, p.end_date >= CURRENT_DATE AS is_active
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
                SELECT p.package_id, p.title, p.start_date, p.end_date, d.location as depot_name, p.end_date >= CURRENT_DATE AS is_active
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
                'start_date': package[2].strftime('%Y-%m-%d'),
                'end_date': package[3].strftime('%Y-%m-%d'),
                'depot_name': package[4],
                'is_active': bool(package[5])
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


@app.route('/employee/edit-package/<int:package_id>', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def editPackage(package_id):
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

        sql_update_package = """
            UPDATE Packages
            SET title = %s, start_date = %s, end_date = %s, depot_id = %s
            WHERE package_id = %s
        """
        updateSQL(sql_update_package, (title, start_date, end_date, depot_id, package_id))

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': f'Database error occurred: {err}'}), 500


@app.route('/employee/toggle-package/<int:package_id>', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def togglePackage(package_id):
    try:
        data = request.json
        current_status = data.get('status')
        new_status = 'Active' if current_status == 'Inactive' else 'Inactive'
        new_end_date = datetime.today().strftime('%Y-%m-%d')
        
        sql_toggle_package = """
            UPDATE Packages
            SET end_date = %s
            WHERE package_id = %s
        """
        updateSQL(sql_toggle_package, (new_end_date, package_id))

        return jsonify({'status': True, 'new_status': new_status})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred: {err}'}), 500

@app.route('/employee/box-products/<int:package_id>')
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manage_box_products(package_id):
    try:
        sql_package = "SELECT package_id, title, start_date, end_date, depot_id FROM Packages WHERE package_id = %s"
        package = fetchOne(sql_package, (package_id,), withDescription=True)

        if not package:
            return "Package not found", 404

        sql_boxes = "SELECT box_id, box_type, price, quantity, product_id FROM Boxes WHERE package_id = %s"
        existing_boxes = fetchAll(sql_boxes, (package_id,))
        box_types = ['Small', 'Medium', 'Large']
        boxes = {box_type: {'box_id': None, 'price': 0.00, 'quantity': 0, 'products': [], 'product_id': None} for box_type in box_types}

        for box in existing_boxes:
            box_data = {
                'box_id': box[0],
                'price': box[2],
                'quantity': box[3],
                'product_id': box[4],
                'products': fetchAll("""
                    SELECT bi.product_id, p.name, bi.quantity
                    FROM BoxItems bi
                    JOIN Products p ON bi.product_id = p.product_id
                    WHERE bi.box_id = %s
                """, (box[0],))
            }
            boxes[box[1]] = box_data

        for box_type in box_types:
            if boxes[box_type]['box_id'] is None:
                product_name = f"{box_type} Box"
                sql_insert_product = "INSERT INTO Products (name, depot_id, is_active) VALUES (%s, %s, TRUE)"
                product_id = insertSQL(sql_insert_product, (product_name, package['depot_id']))

                sql_insert_box = "INSERT INTO Boxes (package_id, box_type, price, quantity, product_id) VALUES (%s, %s, %s, %s, %s)"
                box_id = insertSQL(sql_insert_box, (package_id, box_type, 0.00, 0, product_id))
                boxes[box_type]['box_id'] = box_id
                boxes[box_type]['product_id'] = product_id

                # Assign fixed images based on box type
                if box_type == 'Small':
                    fixed_image_url = 'box1.jpg'
                elif box_type == 'Medium':
                    fixed_image_url = 'box2.jpg'
                else:
                    fixed_image_url = 'box3.jpg'

                sql_insert_image = "INSERT INTO ProductImages (product_id, image, is_primary) VALUES (%s, %s, TRUE)"
                insertSQL(sql_insert_image, (product_id, fixed_image_url))

        categories = fetchAll("SELECT category_id, category_name FROM Category")
        products = fetchAll("SELECT product_id, name FROM Products WHERE depot_id = %s", (package['depot_id'],))

        formatted_categories = [{'id': category[0], 'name': category[1]} for category in categories]
        formatted_products = [{'id': product[0], 'name': product[1]} for product in products]

        package_data = {
            'package_id': package['package_id'],
            'title': package['title'],
            'start_date': package['start_date'],
            'end_date': package['end_date'],
            'depot_id': package['depot_id']
        }

        return render_template('manage-box-products.html', package=package_data, boxes=boxes, categories=formatted_categories, products=formatted_products)
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

        sync_boxes_to_products()   

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

@app.route('/employee/update-box-quantity', methods=['POST'])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def update_box_quantity():
    try:
        data = request.json
        box_id = data.get('box_id')
        quantity = data.get('quantity')

        if not all([box_id, quantity]):
            return jsonify({'status': False, 'message': 'All fields are required'}), 400

        sql_update_quantity = """
            UPDATE Boxes
            SET quantity = %s
            WHERE box_id = %s
        """
        updateSQL(sql_update_quantity, (quantity, box_id))

        sync_boxes_to_products()  

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

        sql_insert_box_item = """
            INSERT INTO BoxItems (box_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """
        insertSQL(sql_insert_box_item, (box_id, product_id, quantity))

        sql_get_box_ids = "SELECT box_id, box_type FROM Boxes WHERE package_id = (SELECT package_id FROM Boxes WHERE box_id = %s)"
        boxes = fetchAll(sql_get_box_ids, (box_id,))
        for box in boxes:
            if box[1] == 'Medium':
                medium_quantity = quantity + 1
                insertSQL(sql_insert_box_item, (box[0], product_id, medium_quantity))
            elif box[1] == 'Large':
                large_quantity = quantity + 2
                insertSQL(sql_insert_box_item, (box[0], product_id, large_quantity))

        sync_boxes_to_products()   

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

        sync_boxes_to_products()   

        return jsonify({'status': True})
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': False, 'message': 'Database error occurred'}), 500

def sync_boxes_to_products():
    try:
        sql_select_boxes = """
            SELECT box_id, product_id, price, quantity 
            FROM Boxes
        """
        boxes = fetchAll(sql_select_boxes)

        for box in boxes:
            box_id, product_id, price, quantity = box

            sql_select_box_items = """
                SELECT bi.box_id, bi.quantity, p.name as product_name
                FROM BoxItems bi
                JOIN Products p ON bi.product_id = p.product_id
                WHERE bi.box_id = %s
            """
            box_items = fetchAll(sql_select_box_items, (box_id,))

            box_items_description = "This box contains the following items:\n"
            for item in box_items:
                box_items_description += f" {item[2]}: {item[1]} units ;\n"

            sql_select_product_description = """
                SELECT description
                FROM Products
                WHERE product_id = %s
            """
            current_description = fetchOne(sql_select_product_description, (product_id,))

            if current_description and 'description' in current_description:
                new_description = f"{current_description['description']} {box_items_description}"
            else:
                new_description = box_items_description

            update_query = """
                UPDATE Products
                SET price = %s, 
                    stock = %s, 
                    category_id = 8, 
                    unit_id = 3, 
                    depot_id = 1, 
                    is_active = TRUE,
                    description = %s
                WHERE product_id = %s
            """
            updateSQL(update_query, (price, quantity, new_description, product_id))

        print("Products table successfully updated with Boxes data.")

    except Exception as e:
        print(f"Error: {e}")

sync_boxes_to_products()
