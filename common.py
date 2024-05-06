import uuid, json
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationError
from dbFile.config import fetchOne
from functools import wraps
from flask import session, redirect, url_for


def toDay():
    return datetime.now().strftime('%Y-%m-%d')

def nextMonthDate():
    today = datetime.now()

    next_month_date = today.replace(month=today.month + 1)

    if today.month == 12:
        next_month_date = next_month_date.replace(year=today.year + 1, month=1)

    return next_month_date.strftime('%Y-%m-%d')

def nextYearDate():
    today = datetime.now()

    next_year = today + timedelta(days=365)

    return next_year.strftime("%Y-%m-%d")

def generateImageId():
    """
    Function to generate a unique image ID.

    Returns:
    - str: A string representation of a UUID4, which serves as the image ID.
    """
    image_uuid = uuid.uuid4()
    return str(image_uuid)