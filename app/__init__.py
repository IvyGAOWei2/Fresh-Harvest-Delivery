from flask import Flask
from flask_hashing import Hashing

app = Flask(__name__)
app.static_folder = 'static'
# app.config['UPLOAD_FOLDER'] = '/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/app/static/img'
app.config['UPLOAD_FOLDER'] = 'static/images/upload'
app.secret_key = 'f5c6b877e9e8461192677370eab53b2d'
app.salt = 'group_az'
app.hashing = Hashing(app)


# Consumer and Employees
from app import authenticate
from app import profile

# Consumer
from app import index
from app import shop
from app import cart

# Employees
from app import admin
from app import manage_product
from app import manage_profile
from app import manage_discount