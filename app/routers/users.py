from typing import List
from fastapi import status , HTTPException , Depends , APIRouter
from app.database import Session, get_db
from app import models , schemas , utils

router = APIRouter(
    prefix="/user" , tags=["User"]
)

@router.post("/", response_model=schemas.User_response, status_code=status.HTTP_201_CREATED)
def create_user(user : schemas.User , db : Session = Depends(get_db)):

    hashed_password = utils.hashed_pass(user.user_password)
    user.user_password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[schemas.User_response])
def get_users(db : Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}" , response_model=schemas.User_response)
def get_user(user_id : int , db : Session = Depends(get_db) ):

    matching_user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not matching_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No user found with id : {user_id}")
    
    return matching_user