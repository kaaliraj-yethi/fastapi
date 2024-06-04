from sqlalchemy.orm import Session

import models,schemas

#to get user from user id
def get_user (db:Session, User_id : int):
    return db.query(models.User).filter(models.User.id == User_id).first()


#d get user from email_id 
def get_user_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()


#get all users
# 
def get_users(db:Session,skip:int = 0 , limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

#create user
def create_user (db:Session, user: schemas.UserCreate) :
    hashed_password = user.password +"hash"
    db_user = models.User(email = user.email, hashed_password = hashed_password)      
    db.add(db_user)
    db.commit()
    return db_user

#get items

def get_items(db:Session, skip: int = 0,limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

#get items of a user

def get_items_for_user(db:Session,user_id:int):
    return db.query(model.Item).filter(models.Item.owner_id == user_id).all()


#create item

def create_item(db:Session,item: schemas.ItemCreate,user_id : int):
    db_item = model.Item(**item.model_dump(),owner_id = user_id)
    db.commit()
    return db_item

