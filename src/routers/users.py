from fastapi import APIRouter
from models import User
from query import registerUser, getUserByUsername

router = APIRouter(
    tags=["Users"]
)

@router.get("/user/{username}", response_model=User | None)
async def getusers(username: str):
    user = await getUserByUsername(username)
    if user:
        return user
    return None

@router.post("/user/add/",response_model=bool)
async def adduser(user: User):
    userdb = await registerUser(user)
    return userdb==True
