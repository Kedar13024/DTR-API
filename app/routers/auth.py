from fastapi import status , HTTPException , Depends , APIRouter
from app.database import Session, get_db
from app import models , schemas , utils


router = APIRouter(
    prefix="/login" , tags=["Authentication"]
)

@router.post("/")
def login(user_credentials :schemas.User_login , db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.user_email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Invalid credentials!")

    if not utils.verify_pass(user_credentials.password , user.user_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Invalid credentials!")

    return {"token" : "sample_token"}
