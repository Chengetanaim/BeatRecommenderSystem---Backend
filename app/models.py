from .database import Base
from sqlalchemy import Integer, String, Boolean, Column, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profession = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "users_profile"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    location = Column(String, nullable=False)
    favourite_genre = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    user = relationship("User", back_populates="profile")

    @property
    def age(self):
        age = datetime.now().date() - self.date_of_birth
        return round(age.days / 365.25)
