from app import app
from flask import render_template, request
from dbFile.config import fetchAll, updateSQL
import os

# User-defined function
from dbFile.config import updateSQL, insertSQL
from common import roleRequired, validateProductProfile, getImageExt, generateImageId

# Function to save uploaded images
def saveImage(img):
    # Get the file extension of the uploaded image
    ext = getImageExt(img.filename)

    # Check if the extension is valid
    if not ext:
        return ext

    # Generate a unique image name using a custom function
    image_name = generateImageId() + '.' + ext
    # Construct the full path where the image will be saved
    filename = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], image_name)

    # Save the uploaded image to the specified location
    img.save(filename)
    # Return the name of the saved image
    return 'upload/' + image_name


@app.route("/product/list", methods = ["GET"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def manageProduct():
    sql_products = """
        SELECT 
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            p.category_id,
            p.unit_id,
            p.depot_id,
            PI.image AS image
        FROM 
            Products p
        INNER JOIN 
            Category c ON p.category_id = c.category_id
        INNER JOIN 
            Unit u ON p.unit_id = u.unit_id
        INNER JOIN 
            Depots d ON p.depot_id = d.depot_id
        INNER JOIN 
            ProductImages PI ON p.product_id = PI.product_id
        AND p.is_active = True;
    """
    product_list = fetchAll(sql_products, None, True)
    return render_template('manage-products.html', productList = product_list, categoryList=app.category_list, unitList=app.unit_list, depotList=app.depot_list)


@app.route("/product/add",methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def addProduct():
    data = dict(request.form)

    product_id = insertSQL("INSERT INTO Products (name, category_id, unit_id, depot_id, price, stock, description) VALUES (%s, %s, %s, %s, %s, %s, %s);", \
        (data['name'], data['category_id'], data['unit_id'], data['depot_id'], data['price'],data['stock'], data['description']))

    image_name = saveImage(request.files['image'])
    img_id = insertSQL("INSERT INTO ProductImages (product_id, image, is_primary, is_deleted) VALUES (%s, %s, %s, %s);", (product_id, image_name, True, False))

    if product_id:
        return {"status": True}, 200
    else:
        return {"status": False}, 500


@app.route("/product/update", methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def updateProduct():
    verified_data = validateProductProfile(request.form.to_dict())

    product_id = verified_data['product_id']
    verified_data.pop('product_id')

    if verified_data:
        updates,params = [], []
        for key, value in verified_data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(product_id)

    update_successful = updateSQL("UPDATE Products SET " + ", ".join(updates) + " WHERE product_id = %s", params)
    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500

@app.route("/product/delist", methods = ["POST"])
@roleRequired(['Staff', 'Local_Manager', 'National_Manager'])
def productDelist():
    data = request.get_json()

    update_successful = updateSQL("UPDATE Products SET is_active = FALSE WHERE product_id = %s;", (data['product_id'],))

    if update_successful:
        return {"status": True}, 200
    else:
        return {"status": False}, 500