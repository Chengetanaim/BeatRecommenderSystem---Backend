from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from ... import models, utils
from ...database import get_db
from ...oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/login")
def login(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(
            (models.User.email == credentials.username)
            | (models.User.username == credentials.username)
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
        )
    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
        )
    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "toke_type": "bearer"}
