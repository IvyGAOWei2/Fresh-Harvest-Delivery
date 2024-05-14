import uuid, json
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationError
from dbFile.config import fetchOne
from functools import wraps
from flask import session, redirect, url_for


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
