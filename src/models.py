from odmantic import Model
from pydantic import BaseModel
from odmantic import Field, Index
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserName(BaseModel):
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

#DB Schema

class User(Model):
    firstname: str
    lastname: str
    image: str | None = None
    username: str = Field(index = True, unique = True)
    email: str = Field(index = True, unique = True)
    password: str

    model_config = {
            "indexes": lambda: [
                Index(User.username, unique=True),
                Index(User.email, unique=True),
            ]
    }

class UserSaved(Model):
    user: str
    post: list

class UserReactions(Model):
    user: str
    post: str
    reaction: str

class Post(Model):
    user: str
    title: str
    content: str
    image: str
    views: int
    reactions: int
    date: datetime
    tags: list

class Comment(Model):
    user: str
    post: str
    content: str
    date: datetime



DBMODEL = [User, UserSaved, UserReactions, Post, Comment]
