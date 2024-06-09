import uuid, os, random, string, time
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationError
from dbFile.config import fetchOne
from functools import wraps
from flask import session, redirect, url_for, abort
from configparser import RawConfigParser

# Model for user login
class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=50)
    is_saved: Optional[str] = Field(None, min_length=1, max_length=1)

# Model for consumer register
class Register(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=50)
    given_name: str = Field(min_length=1, max_length=35)
    family_name: str = Field(min_length=1, max_length=35)
    phone: int = Field(ge=1, le=9999999999999)
    address: str = Field(min_length=1, max_length=80)
    postcode:str = Field(min_length=1, max_length=4)
    depot_id: int = Field(ge=1, le=10)

# Model for employee register
class RegisterEmployee(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=50)
    given_name: str = Field(min_length=1, max_length=35)
    family_name: str = Field(min_length=1, max_length=35)
    phone: int = Field(ge=1, le=9999999999999)
    address: str = Field(min_length=1, max_length=80)
    depot_id: int = Field(ge=1, le=10)
    hire_date: datetime = Field(None)

# Model for consumer profile
class consumerProfile(BaseModel):
    user_id: int = Field(ge=1, le=999)
    given_name: Optional[str] = Field(None, min_length=1, max_length=35)
    family_name: Optional[str] = Field(None, min_length=1, max_length=35)
    address: Optional[str] = Field(None, min_length=1, max_length=80)
    postcode: Optional[str] = Field(None, min_length=1, max_length=4)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, min_length=1, max_length=13)
    depot_id: Optional[int] = Field(None, ge=1, le=10)
    new_password: Optional[str] = Field(None, min_length=1, max_length=50)
    old_password: Optional[str] = Field(None, min_length=1, max_length=50)

# Model for employee profile
class employeeProfile(BaseModel):
    user_id: int = Field(ge=1, le=999)
    given_name: Optional[str] = Field(None, min_length=1, max_length=35)
    family_name: Optional[str] = Field(None, min_length=1, max_length=35)
    address: Optional[str] = Field(None, min_length=1, max_length=80)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, min_length=1, max_length=13)
    hire_date: Optional[datetime] = Field(None)
    depot_id: Optional[int] = Field(None, ge=1, le=10)
    type:Optional[str] = Field(None)
    new_password: Optional[str] = Field(None, min_length=1, max_length=50)
    old_password: Optional[str] = Field(None, min_length=1, max_length=50)

# Model for product profile
class productProfile(BaseModel):
    product_id: int = Field(ge=1, le=999)
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=1000)
    price: str = Field(min_length=1, max_length=50)
    stock: int = Field(ge=1, le=999)
    category_id: int = Field(ge=1, le=999)
    unit_id: int = Field(ge=1, le=999)
    depot_id: int = Field(ge=1, le=999)

def roleRequired(roles):
    """ 装饰器用于在允许访问特定路由之前检查用户角色。"""
    def decorator(func):
        """ 包装原始函数的装饰器函数。 """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            """ 检查用户角色的装饰函数 """
            if not session.get('loggedin'):
                return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面。
            
            user_type = session.get('type')
            if not user_type or user_type not in roles:
                abort(403)  # 如果用户未被授权，则中止请求并返回403 Forbidden状态码。
            
            return func(*args, **kwargs)  # 如果用户具有所需角色，则返回原始函数的结果。
        
        return decorated_function
    return decorator

def validateLogin(data):
    try:
        return Login(**data)
    except ValidationError as e:
        # print(e.errors())
        return False

def validateRegister(data):
    try:
        return Register(**data)
    except ValidationError as e:
        # print(e.errors())
        return False

def validateRegisterEmployee(data):
    try:
        return RegisterEmployee(**data)
    except ValidationError as e:
        # print(e.errors())
        return False

def validateEmail(email):
    return fetchOne('SELECT user_id FROM Users WHERE email = %s AND is_deleted = FALSE', (email,))

def validateUserAccount(email):
    return fetchOne('SELECT * FROM Users WHERE email = %s AND is_deleted = FALSE', (email,), True)

def validateEmployeeProfile(data):
    try:
        profile = employeeProfile(**data)
        return profile.model_dump(exclude_none=True)
    except ValidationError as e:
        # print(e.errors())
        return False

def validateConsumerProfile(data):
    try:
        profile = consumerProfile(**data)
        return profile.model_dump(exclude_none=True)
    except ValidationError as e:
        # print(e.errors())
        return False

def validateProductProfile(data):
    try:
        product = productProfile(**data)
        return product.model_dump(exclude_none=True)
    except ValidationError as e:
        # print(e.errors())
        return False

def getUserProfile(id, type):
    user_table = {'Consumer': 'Consumer'}.get(type, 'Employees')

    return fetchOne('SELECT * FROM ' + user_table +' WHERE user_id = %s;', (id,), True)

def fakeReview():
    Reviews = [{'user_name': 'David', 'rating': 5, 'img': 'user_default_image.png', 'depot_location': 'Invercargill', 'product_id': 999, 'review_date': 'Mar 14, 2024', 'review_text': "I love the variety of fresh fruits and vegetables available at Fresh Harvest. It's great to be able to support local farmers and enjoy the taste of seasonal produce. The online ordering system is convenient, and the customer service is excellent."},
    {'user_name': 'Emily', 'rating': 4, 'img': 'user_default_image.png', 'depot_location': 'Hamilton', 'product_id': 999, 'review_date': 'Jan 05, 2024', 'review_text': "As a café owner, quality produce is essential for our business. Fresh Harvest has been our go-to supplier for fresh herbs and vegetables. Their account holder system is fantastic, allowing us to manage our orders and invoices efficiently. Their end-of-month payment option has really helped us streamline our operations."},
    {'user_name': 'Michael', 'rating': 5, 'img': 'user_default_image.png', 'depot_location': 'Auckland', 'product_id': 999, 'review_date': 'Sep 26, 2023', 'review_text': "I’ve been ordering from Fresh Harvest for over a year, and the quality of the produce always impresses me. The vegetables are fresh, and the delivery is always on time. Being able to order a mixed box on a subscription has made my grocery shopping so much easier. Plus, the staff is always helpful whenever I have a query"},
    {'user_name': 'Sarah', 'rating': 5, 'img': 'user_default_image.png', 'depot_location': 'Wellington', 'product_id': 999, 'review_date': 'May 03, 2024', 'review_text': "As a busy professional, Fresh Harvest has been a lifesaver. Their pre-made boxes are perfect for quick and healthy meals. The delivery service is reliable, and the quality of the produce is always top-notch."}]

    return random.sample(Reviews, 3)

def toDay():
    return datetime.now().strftime('%Y-%m-%d')

def yesterDay():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def getImageExt(filename):
    try:
        ext_name = filename.rsplit('.', 1)[1].lower()
        return ext_name if ext_name in ['png', 'jpg', 'jpeg', 'gif'] else None
    except (IOError, SyntaxError) as e:
        return None

def generateImageId():
    image_uuid = uuid.uuid4()
    return str(image_uuid)

def generateCode(length):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def getTimestamp(hours=0):
    timestamp = int(time.time()) + (hours * 3600)
    return timestamp

def validateConsumerEmail(email):
    return fetchOne('SELECT user_id FROM Users WHERE email = %s AND is_deleted = FALSE AND type = "Consumer"', (email,))

def saveImage(upload_folder, img):
    # Get the file extension of the uploaded image
    ext = getImageExt(img.filename)

    # Check if the extension is valid
    if not ext:
        return ext

    # Generate a unique image name using a custom function
    image_name = generateImageId() + '.' + ext
    # Construct the full path where the image will be saved
    filename = os.path.join(upload_folder, image_name)

    # Save the uploaded image to the specified location
    img.save(filename)
    # Return the name of the saved image
    return image_name

def emailOrder(order_id):
    return fetchOne("SELECT o.order_date, u.email, c.given_name FROM Orders o \
        JOIN Users u ON o.user_id = u.user_id \
        JOIN Consumer c ON u.user_id = c.user_id \
        WHERE o.order_id = %s",  (order_id,), True)

def newShipping(new):
    try:
        config = RawConfigParser()
        config.read('app/config.ini')
        config.set('base', 'shipping', new)

        with open('app/config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        return False
    else:
        return True
