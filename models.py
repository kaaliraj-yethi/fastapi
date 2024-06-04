from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Table
from sqlalchemy.orm import relationship
from db import Base

like_posts = Table(
"like_posts",
Base.metadata,
Column("post_id",Integer,ForeignKey("posts.id")),
Column("User_id",Integer,ForeignKey("users.id")),

)



class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email = Column (String,unique=True,index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    
    items = relationship("Item",back_populates="owner")
    posts = relationship("Post",back_populates="author")
    posts_liked = relationship("Post",secondary= like_posts,back_populates= "liked_by_users")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True)
    tittle = Column(String)
    description = Column(String)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User",back_populates = "items")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key = True)
    content = Column(String)
    author_id = Column(Integer,ForeignKey("users.id"))
    author = relationship("User",back_populates = "posts")
    liked_by_users = relationship("User",secondary = like_posts,back_populates = "posts_liked")
