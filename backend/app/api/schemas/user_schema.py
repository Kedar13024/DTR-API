"""Pydantic schemas and role enum for user accounts."""

from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class INphone(PhoneNumber):
    """Validate phone numbers using India's default region and E.164 format."""

    default_region_code = 'IN'
    phone_format = "E164"

class UserRole(StrEnum):
    """Roles assigned to registered users."""

    CITIZEN = "citizen"
    RESPONDER = "responder"
    ADMIN = "admin"


class User(BaseModel):
    """Validate data required to register a user.

    Attributes:
        user_fullname: User's full name.
        user_phoneNo: User's phone number.
        user_email: User email address.
        user_password: Plain-text password received during registration.
    """
    user_fullname : str
    user_phoneNo : INphone
    user_email : EmailStr
    user_password : str

class User_login(BaseModel):
    """Validate a user's login credentials.

    Attributes:
        email: User email address.
        password: Plain-text password.
    """

    email : EmailStr
    password : str

class User_response(BaseModel):
    """Serialize non-sensitive user information in API responses.

    Attributes:
        user_id: Unique user identifier.
        user_email : User email
        created_at: Timestamp when the user was created.
    """
    
    model_config=ConfigDict(from_attributes = True)

    user_id : int
    user_email : EmailStr
    created_at : datetime
