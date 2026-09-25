"""JWT creation, validation, and current-user dependencies."""

from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from datetime import UTC, timedelta ,datetime
from backend.app.api.core.config import settings
from backend.app.api.db.database import Session, get_db
from backend.app.api.models.models import User
from backend.app.api.schemas.token_schema import TokenData
from backend.app.api.schemas.user_schema import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    """Create a JWT with an expiration time.

    Args:
        data: Claims to encode into the token.

    Returns:
        str: Signed JWT access token.
    """


    to_encode = data.copy()

    expire_time = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str , credential_exception):
    """Decode a JWT and extract its authenticated user ID.

    Args:
        token: JWT access token to validate.
        credential_exception: Exception raised for an invalid token.

    Returns:
        TokenData: User data extracted from the valid token.

    Raises:
        HTTPException: If the token is malformed, expired, or lacks a user ID.
    """


    try:

        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])

        current_user_id : str = payload.get("user_id")

        if current_user_id is None:
            raise credential_exception

        token_data = TokenData(user_id=current_user_id)

    except JWTError as exc:
        raise credential_exception from exc

    return token_data


def get_current_user(token : str = Depends(oauth2_scheme) , db : Session = Depends(get_db)):
    """Retrieve the database user represented by the bearer token.

    Args:
        token: Bearer token extracted by FastAPI.
        db: Database session supplied by FastAPI.

    Returns:
        User: Authenticated user record.

    Raises:
        HTTPException: If the bearer token is invalid.
    """

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Could not validiate credentials" , headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token , credentials_exception)

    user = db.query(User).filter(User.user_id == token.user_id).first()
    if user is None:
        raise credentials_exception

    return user

def require_admin(current_user : User = Depends(get_current_user)):
    if current_user.user_role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Access denied. Only administrators can perform this action.")
    return current_user
