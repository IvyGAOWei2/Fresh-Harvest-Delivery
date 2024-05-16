import uuid, json
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationError
from dbFile.config import fetchOne
from functools import wraps
from flask import session, redirect, url_for, abort


# Model for user login
class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=50)
    is_saved: Optional[str] = Field(None, min_length=1, max_length=1)

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

def validateUserAccount(email):
    return fetchOne('SELECT * FROM Users WHERE email = %s AND is_deleted = FALSE', (email,), True)

def validateEmployeeProfile(data):
    try:
        profile = employeeProfile(**data)
        return profile.model_dump(exclude_none=True)
    except ValidationError as e:
        # print(e.errors())
        return False

def getUserProfile(id, type):
    user_table = {'Consumer': 'Consumer'}.get(type, 'Employees')

    return fetchOne('SELECT * FROM ' + user_table +' WHERE user_id = %s;', (id,), True)
