from pydantic import BaseModel

class ItemBase (BaseModel):
    tittle: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

class config:
    orm_mode = True

class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:int
    is_active: bool
    items : list[Item] = [] 

class config:
    orm_mode = True
