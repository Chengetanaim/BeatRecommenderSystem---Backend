from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class Profession(Enum):
    Rapper = "Rapper"
    Producer = "Producer"


class Gender(Enum):
    Male = "Male"
    Female = "Female"


class Location(Enum):
    Harare = "Harare"
    Chinhoyi = "Chinhoyi"
    Kadoma = "Kadoma"
    Chegutu = "Chegutu"
    Kwekwe = "Kwekwe"
    Gweru = "Gweru"
    Bulawayo = "Bulawayo"
    Shurugwi = "Shurugwi"
    Masvingo = "Masvingo"
    Mutare = "Mutare"
    Chitungwiza = "Chitungwiza"
    Marondera = "Marondera"
    VictoriaFalls = "VictoriaFalls"
    Bindura = "Bindura"
    Zvishavane = "Zvishavane"
    Kariba = "Kariba"
    Hwange = "Hwange"
    Norton = "Norton"


class Genre(Enum):
    Trap = "Trap"
    Drill = "Drill"
    LofiHipHop = "LofiHipHop"
    ConsciousRap = "ConsciousRap"
    EmoRap = "EmoRap"
    MelodicRap = "MelodicRap"
    AfroBeatRap = "AfroBeatRap"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    profession: Profession


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime


class UserProfileBase(BaseModel):
    user_id: int
    date_of_birth: datetime
    gender: Gender
    location: Location
    favourite_genre: Genre


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileResponse(UserProfileBase):
    id: int
    created_at: datetime
