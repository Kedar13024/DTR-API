"""Password hashing and verification utilities."""

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"] , deprecated = "auto")

def hashed_pass(password :str):
    """Hash a plain-text password with Argon2.

    Args:
        password: Plain-text password to protect.

    Returns:
        str: Secure Argon2 password hash.
    """

    return  pwd_context.hash(password)

def verify_pass(password : str , hashedPassword : str):
    """Verify a plain-text password against an existing hash.

    Args:
        password: Plain-text password supplied by the user.
        hashedPassword: Stored Argon2 password hash.

    Returns:
        bool: True when the password matches the hash; otherwise, False.
    """

    return pwd_context.verify(password , hashedPassword)
