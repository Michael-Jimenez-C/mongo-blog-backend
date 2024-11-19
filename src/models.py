from types import NoneType
from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserName(BaseModel):
    username: str

class User(BaseModel):
    firstname: str
    lastname: str
    image: str | None = None
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserPreferences(BaseModel):
    theme: str

class UserSaved(BaseModel):
    user: str
    post: list

class UserReactions(BaseModel):
    user: str
    post: str
    reaction: str

class Post(BaseModel):
    user: str
    title: str
    content: str
    image: str
    views: int
    reactions: int
    date: datetime
    tags: list

class Comment(BaseModel):
    user: str
    post: str
    content: str
    date: datetime
