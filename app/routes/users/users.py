from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import desc
from ... import models, schemas, utils
from ...database import get_db
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])

db_session = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: db_session):
    users = db.query(models.User).order_by(desc(models.User.created_at))
    return users


@router.post(
    "/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: db_session):
    existing_user = (
        db.query(models.User)
        .filter(
            (models.User.username == user.username) | (models.User.email == user.email)
        )
        .first()
    )
    if existing_user:
        conflict_detail = (
            "User with this username already exists"
            if existing_user.username == user.username
            else "User with this email already exists"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=conflict_detail
        )

    user.password = utils.hash_password(user.password)
    user.profession = user.profession.value
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: db_session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
