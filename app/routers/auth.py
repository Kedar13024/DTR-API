from fastapi import status , HTTPException , Depends , APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.database import Session, get_db
from app import models, schemas , utils
from app.routers.oauth2 import create_access_token


router = APIRouter(
    prefix="/login" , tags=["Authentication"]
)

@router.post("/" , response_model=schemas.Token_base)
def login(user_credentials :OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.user_email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid credentials!")

    if not utils.verify_pass(user_credentials.password , user.user_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid credentials!")

    access_token = create_access_token(data={"user_id" : user.user_id})
    return {"access_token" : access_token , "token_type" : "bearer"}
