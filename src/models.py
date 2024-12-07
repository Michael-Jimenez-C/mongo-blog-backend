from odmantic import Model
from pydantic import BaseModel
from odmantic import Field, Index, EmbeddedModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserName(BaseModel):
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class ChangeEmail(BaseModel):
    email: str
    password: str

class ChangeUserInformation(BaseModel):
    firstname: str
    lastname: str
    birth_date: datetime
    display_name: str | None = None
    image: str | None = None



#DB Schema

class UserPreferences(EmbeddedModel):
    notifications: bool = False
    theme: str = "dark"
    public_profile: bool = True
    email_notifications: bool = False

class User(Model):
    firstname: str
    lastname: str
    image: str | None = None
    username: str = Field(index = True, unique = True)
    display_name: str | None = None
    email: str = Field(index = True, unique = True)
    birth_date: datetime
    password: str
    settings: UserPreferences

    model_config = {
            "indexes": lambda: [
                Index(User.username, unique=True),
                Index(User.email, unique=True),
            ]
    }

class UserSaved(Model):
    user: str = Field(index = True, unique = True)
    post: list
    model_config = {
            "indexes": lambda: [
                Index(UserSaved.user)
            ]
    }

class UserReactions(Model):
    user: str = Field(index = True, unique = True)
    post: str
    reaction: str
    model_config = {
            "indexes": lambda: [
                Index(UserReactions.user)
            ]
    }

class Post(Model):
    post: str = Field(index = True, unique = True)
    user: str = Field(index = True, unique = True)
    title: str = Field(index = True)
    content: str
    image: str
    views: int
    reactions: int
    date: datetime
    tags: list
    model_config = {
            "indexes": lambda: [
                Index(Post.post, unique = True),
                Index(Post.user),
                Index(Post.title)
            ]
    }

class Comment(Model):
    user: str
    post: str = Field(index = True, unique = True)
    content: str
    date: datetime
    model_config = {
            "indexes": lambda: [
                Index(Comment.post)
            ]
    }


DBMODEL = [User, UserSaved, UserReactions, Post, Comment]
