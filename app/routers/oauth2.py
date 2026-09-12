from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from datetime import UTC, timedelta ,datetime
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import Token_base, Token_data

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):

    to_encode = data.copy()

    expire_time = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : Token_base , credential_exception):

    try:

        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])

        current_user_id : str = payload.get("user_id")

        if current_user_id is None:
            raise credential_exception

        token_data = Token_data(user_id=current_user_id)

    except JWTError as exc:
        raise credential_exception from exc

    return token_data


def get_current_user(token : str = Depends(oauth2_scheme) , db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Could not validiate credentials" , headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token , credentials_exception)

    user = db.query(User).filter(User.user_id == token.user_id).first()

    return user