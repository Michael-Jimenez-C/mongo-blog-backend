from fastapi import FastAPI
from models import User, UserPreferences, UserSaved, UserReactions, Post, Comment
from query import registerUser, getUserByUsername

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/validate")
async def validate():
    pass


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
