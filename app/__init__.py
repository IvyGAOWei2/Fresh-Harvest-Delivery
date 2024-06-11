from flask import Flask
from flask_hashing import Hashing
from configparser import RawConfigParser

# User-defined function
from dbFile.config import fetchAll

config = RawConfigParser()
config.read('app/config.ini')
# config.read('/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/app/config.ini')

app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'app/static/images/upload'
# app.config['UPLOAD_FOLDER'] = '/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/app/static/images/upload'
app.config['PRODUCT_UPLOAD_FOLDER'] = 'app/static/images/product/upload'
# app.config['PRODUCT_UPLOAD_FOLDER'] = '/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/app/static/images/product/upload'
app.secret_key = 'f5c6b877e9e8461192677370eab53b2d'
app.salt = 'group_az'
app.shipping = int(config['base']['shipping'])
app.category_list = fetchAll("""SELECT * FROM Category;""", None, True)
app.unit_list = fetchAll("""SELECT * FROM Unit;""", None, True)
app.depot_list = fetchAll("""SELECT * FROM Depots WHERE location != 'NZ';""", None, True)
app.giftcard_list = [item[0] for item in fetchAll("SELECT product_id FROM Products WHERE category_id = 6")]
app.send_email = False
app.hashing = Hashing(app)


# Consumer and Employees
from app import authenticate
from app import profile
from app import order_history

# Consumer
from app import index
from app import shop
from app import cart
from app import consumer_points
from app import consumer_box

# Employees
from app import admin
from app import manage_product
from app import manage_profile
from app import manage_discount
from app import manage_news



# National_Manager
from app import manage_system_settings
from app import manage_giftcards
from app import manage_application
from app import manage_boxes
from app import manage_points
