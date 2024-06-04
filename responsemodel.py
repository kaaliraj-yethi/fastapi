from fastapi import FastAPI
from pydantic import BaseModel


class BaseUser(BaseModel):
    username:str
    name: str
    email: str

class UserIn (BaseUser):
    password: str
    
class UserInDB(BaseUser):
    hashed_password : str

class UserOut(BaseUser):
    pass

def hashing_password(password: str):
    return "random_hash"+password


def save_user(user: UserIn):
    hashed_password = hashing_password(user.password)
    user_in_db = UserInDB(**user.model.dump(),hashed_password=hashed_password)
    print("user saved to db")
    return user_in_db


app = FastAPI()




@app.post("/user",response_model = UserOut,response_model_exclude = ["username"] )
def create_user(user: UserIn) -> UserIn:
    user_in_db = save_user(user)
    return user_in_db
