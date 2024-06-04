from pydantic import BaseModel
from datetime import datetime


class Userbase(BaseModel):
    username : str
    email : str

class UserCreate(Userbase):
    password: str

class User(Userbase):
    created_dt: datetime

class Config:
    orm_mode = True

class UserUpdate(BaseModel):
    email: str


    





    