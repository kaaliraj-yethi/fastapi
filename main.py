from fastapi  import FastAPI,Depends
from db import SessionLocal ,engine
import models,schemas,service
from db import get_db

from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind= engine)

app = FastAPI()


@app.post("/users", response_model = schemas.User )
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    db_user = service.get_user_by_email(db,user.email)
    if db_user:
        raise HTTPException(status_code = 400,detail = "Email already in use")
    db_user = service.create_user(db,user)
    return db_user


@app.get("/users",response_model = list[schemas.User]) 
def get_users(skip: int = 0 , limit: int= 100, db:Session = Depends(get_db)) :
    users = service.get_users(db,skip,limit)
    return users


@app.get("/users/{user_id}", response_model = schemas.User)
def get_user(user_id: int , db: Session = Depends(get_db)):
    db_user = service.get_user(db,user_id)
    if db_user is None:
        raise HTTPException(status_code= 404,Detail = "User not found")
    return db_user



