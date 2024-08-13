from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


SQLALCHEMY_DATABASE_URL = f"postgresql://che:kVRcWqCubbzN29SRh5yt0OnplR8LxGEj@dpg-cqtkonlds78s739oaocg-a/beat_recommender_system"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
