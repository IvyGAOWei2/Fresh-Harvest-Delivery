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


def validateLogin(data):
    try:
        return Login(**data)
    except ValidationError as e:
        # print(e.errors())
        return False

def validateUserAccount(email):
    return fetchOne('SELECT * FROM Users WHERE email = %s AND is_deleted = FALSE', (email,), True)

def getUserProfile(id, type):
    user_table = {'Consumer': 'Consumer'}.get(type, 'Employees')

    return fetchOne('SELECT * FROM ' + user_table +' WHERE user_id = %s;', (id,), True)