from fastapi import FastAPI,Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from models import User as UserModel
from schemas import User as UserSchema , UserCreate , UserUpdate
from database import get_db
from database import Base, engine

import service


app = FastAPI()

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.post("/signup",status_code = status.HTTP_201_CREATED)
async def create_user (user: UserCreate,db:Session = Depends(get_db)):
    db_user = await service.existing_user(db,user.username,user.email)
    if db_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="username or email already in use"
        )

    db_user = await service.create_user(db,user)
    access_token = await service.create_access_token (db_user.id,db_user.username)
    return{

        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username,    
        }


@app.post("/token")
async def login(form_data : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    db_user = await service.authenticate(db,form_data.username,form_data.password)
    if not db_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail = "incorrect username or password")
    acces_token = await service.create_access_token(db_user.id,db_user.username)
    return {
        "access_token ": acces_token,
        "token_type": "bearer"
    }


@app.get("/profile",response_model = UserSchema)
async def get_current_user(token: str, db:Session = Depends(get_db)):
    db_user = await service.get_current_user(db,token)
    if not db_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "you are not authenticated")
    return db_user


@app.put("/users/{username}",status_code = status.HTTP_204_NO_CONTENT)
async def update_user(username : str,token : str ,user: UserUpdate, db: Session = Depends(get_db)):
    #verify token
    db_user = await service.get_current_user(db,token)
    if not db_user or db_user.username != username:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail= "you are not authorised to update this user")
    db_user = await service.update_user(db,db_user,user)


@app.post("/resetpassword/sendcode")
async def reset_send_code(email: str,db: Session = Depends(get_db)):
    db_user = await service.existing_user(db,"",email)
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "user with email not found")
    code = await service.generate_code(db,email)
    await service.fake_email_send(email,code)
    return code


@app.get("/resetpassword/verifycode")
async def reset_verify_code(email: str,code: str,db: Session = Depends(get_db)):
    return await service.verify_code(db,email,code)



@app.put("/resetpassword/reset",status_code = status.HTTP_204_NO_CONTENT)
async def reset_password(email: str, password: str,db: Session = Depends(get_db)):
    db_user = await service.existing_user(db,"",email)
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "user not found")
    await service.update_password(db,db_user,password)




