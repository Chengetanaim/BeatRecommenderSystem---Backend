from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import desc
from ... import models, schemas, utils
from ...database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Response
from ...oauth2 import get_current_user


router = APIRouter(prefix="/user_profiles", tags=["User Profiles"])

db_session = Annotated[Session, Depends(get_db)]
db_current_user = Annotated[schemas.UserResponse, Depends(get_current_user)]


@router.get("/", response_model=schemas.UserProfileResponse)
def get_my_user_profile(db: db_session, current_user: db_current_user):
    my_user_profile = (
        db.query(models.UserProfile)
        .filter(models.UserProfile.user_id == current_user.id)
        .first()
    )
    if not my_user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not created your user profile yet.",
        )
    return my_user_profile


@router.post(
    "/", response_model=schemas.UserProfileResponse, status_code=status.HTTP_201_CREATED
)
def create_my_user_profile(
    my_user_profile: schemas.UserProfileCreate,
    db: db_session,
    current_user: db_current_user,
):
    existing_user_profile = (
        db.query(models.UserProfile)
        .filter(models.UserProfile.user_id == current_user.id)
        .first()
    )
    if existing_user_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have a user profile.",
        )
    my_user_profile.gender = my_user_profile.gender.value
    my_user_profile.favourite_genre = my_user_profile.favourite_genre.value
    my_user_profile.location = my_user_profile.location.value
    db_user_profile = models.UserProfile(
        **my_user_profile.model_dump(), user_id=current_user.id
    )
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)
    return db_user_profile


@router.put(
    "/",
    response_model=schemas.UserProfileResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def edit_my_user_profile(
    my_user_profile: schemas.UserProfileCreate,
    db: db_session,
    current_user: db_current_user,
):
    existing_user_profile_query = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    )
    existing_user_profile = existing_user_profile_query.first()
    if not existing_user_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven't created a profile yet",
        )
    my_user_profile.gender = my_user_profile.gender.value
    my_user_profile.location = my_user_profile.location.value
    my_user_profile.favourite_genre = my_user_profile.favourite_genre.value
    my_user_profile_dict = my_user_profile.model_dump()
    my_user_profile_dict["user_id"] = current_user.id
    existing_user_profile_query.update(my_user_profile_dict, synchronize_session=False)
    db.commit()
    db.refresh(existing_user_profile)
    return existing_user_profile
