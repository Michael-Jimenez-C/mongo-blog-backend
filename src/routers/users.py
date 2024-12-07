from fastapi import APIRouter, Depends
from models import User, UserName, PasswordChange, ChangeEmail, ChangeUserInformation, UserPreferences
from query import registerUser, getUserByUsername, removeUser, changePassword, changeEmail
from .oauth.oauth import get_current_user
from typing_extensions import Annotated

router = APIRouter(
    tags=["Users"]
)

@router.get("/user/{username}", response_model=User | None)
async def getUsers(username: str):
    user = await getUserByUsername(username)
    if user:
        return user
    return None

@router.post("/user/add/",response_model=bool)
async def addUser(user: User):
    userdb = await registerUser(user)
    return userdb==True

@router.delete("/user/deleteAcount",response_model=bool)
async def deleteAcount(current_user: Annotated[UserName, Depends(get_current_user)]):
    res = await removeUser(current_user.username)
    return res

@router.put("/user/updatePassword",response_model=bool)
async def updateUserPasword(password: PasswordChange, current_user: Annotated[UserName, Depends(get_current_user)]):
    r = await changePassword(current_user, password)
    return r

@router.put("/user/updateInformation",response_model=bool)
async def updateUserInformation(information: ChangeUserInformation, current_user: Annotated[UserName, Depends(get_current_user)]):
    pass

@router.put("/user/updateEmail",response_model=bool)
async def updateUserEmail(email: ChangeEmail, current_user: Annotated[UserName, Depends(get_current_user)]):
    r = await changeEmail(current_user, email)
    return r

@router.put("/user/updatePreferences",response_model=bool)
async def updateUserSettings(preferences: UserPreferences, current_user: Annotated[UserName, Depends(get_current_user)]):
    pass
