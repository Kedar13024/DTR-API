"""Pydantic schemas for access tokens and decoded token claims."""

from pydantic import BaseModel


class TokenBase(BaseModel):
    """Serialize a bearer access token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Represent authenticated user data extracted from a JWT."""

    user_id: int | None = None
