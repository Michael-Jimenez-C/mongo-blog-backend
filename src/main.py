from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import User, UserPreferences, UserSaved, UserReactions, Post, Comment
from query import registerUser, getUserByUsername
from routers.oauth import oauth

app = FastAPI()

app.include_router(oauth.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/user/{username}", response_model=User | None)
async def getusers(username: str):
    user = getUserByUsername(username)
    if user:
        return user
    return None

@app.post("/user/add/",response_model=bool)
async def adduser(user: User):
    userdb = registerUser(user)
    return userdb==True
