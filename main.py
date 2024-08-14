from fastapi import FastAPI
from app.database import engine
from app import models
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import users
from app.routes.auth import auth
from app.routes.user_profiles import user_profiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/home")
def index():
    return {"message": "This is home"}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(user_profiles.router)
