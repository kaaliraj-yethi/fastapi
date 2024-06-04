from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from  passlib.context import CryptContext

from random import randint

from models import User as UserModel,ResetPassword as RPModel
from schemas import User as UserSchema , UserCreate , UserUpdate


SECRET_KEY = "mysecretkey"
EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"

OAuth2_bearer = OAuth2PasswordBearer(tokenUrl = "token")
bcrypt_context = CryptContext(schemes = ["bcrypt"])

#signup 
#login



#check exisiting user with same username or email
async def existing_user (db:Session, username:str,email:str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None

 #create token
 # jwt = {encoded data,secret key,algorithm}

async def create_access_token(id: int,username: str):
    encode = {"sub": username,"id":id}
    expires = datetime.utcnow() +timedelta(minutes=EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

#get current user from token

async def get_current_user (db: Session, token: str = Depends(OAuth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        if datetime.frontimestamp(expires) < datetime.utcnow():
            return None

        if username is None or id is None:
            return None

        db_user = db.query(UserModel).filter(UserModel.id == id).first()
        return db_user

    except JWTError:
        return None




#create user

async def create_user (db:Session,user:UserCreate):
    db_user = UserModel(
        username = user.username,
        email = user.email,
        hashed_password = bcrypt_context.hash(user.password)

    )
    db.add(db_user)
    db.commit()
    return db_user

#authenticate

async def authenticate(db: Session,username: str, password: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user:
        return None
    if not bcrypt_context.verify(password,db_user.hashed_password):
        return False
    return db_user


async def update_user(db: Session,db_user:UserModel ,user_update: UserUpdate):
    db_user.email = user_update.email or db_user.email
    db.commit()
    #cloase the database session and restart with selectquery
    db.refresh(db_user)



# reset password funcs


async def generate_code(db: Session, email: str):
    code = str(randint(100000, 999999))
    print(f"Generated code: {code}")  # Debug print to check the generated code

    db_reset = db.query(RPModel).filter(RPModel.email == email).first()
    if db_reset:
        db_reset.code = code
        print(f"Updated existing RPModel with new code: {code}")  # Debug print to confirm code update
    else:
        db_reset = RPModel(email=email, code=code)
        db.add(db_reset)
        print(f"Created new RPModel with code: {code}")  # Debug print to confirm new entry creation

    db.commit()
    return code

async def verify_code (db: Session,email: str,code: str):
    db_reset = db.query(RPModel).filter(RPModel.email == email).first()
    if not db_reset:
        return False
    return db_reset.code == code

async def fake_email_send(email: str,code:str):
    print(f"code sent to {email}")


async def update_password(db: Session,user: UserModel,password: str):
    user.hashed_password = bcrypt_context.hash(password)
    db.commit()


