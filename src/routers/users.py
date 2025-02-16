from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from models import User, UserName, PrivateUser,PasswordChange, ChangeEmail, ChangeUserInformation, UserPreferences, PublicUser
from utils.users_queries import registerUser, getUserByEmail, getUserByUsername, removeUser, changePassword, changeEmail, changeUserInformation, changeUserPreferences
from .oauth.oauth import get_current_user
from typing_extensions import Annotated

router = APIRouter(
    tags=["Users"],
    prefix = "/user"
)

@router.post("/add/",response_model=bool)
async def addUser(user: User):
    r = await registerUser(user)
    return JSONResponse(
        status_code=200,
        content={"message": r}
        )

@router.get("/user/{username}",response_model=PublicUser | None)
async def userInfo(username: str):
    res = await getUserByUsername(username)
    return res

@router.get("/user",response_model=PrivateUser)
async def privateUserInfo(current_user: Annotated[UserName, Depends(get_current_user)]):
    res = await getUserByEmail(current_user.username)
    return res

@router.delete("/deleteAcount",response_model=bool)
async def deleteAcount(current_user: Annotated[UserName, Depends(get_current_user)]):
    res = await removeUser(current_user.username)
    return res

@router.put("/updatePassword",response_model=bool)
async def updateUserPasword(password: PasswordChange, current_user: Annotated[UserName, Depends(get_current_user)]):
    r = await changePassword(current_user, password)
    return r

@router.put("/updateInformation",response_model=bool)
async def updateUserInformation(information: ChangeUserInformation, current_user: Annotated[UserName, Depends(get_current_user)]):
    r = await changeUserInformation(current_user, information)
    return r

@router.put("/updateEmail",response_model=bool)
async def updateUserEmail(email: ChangeEmail, current_user: Annotated[UserName, Depends(get_current_user)]):
    r = await changeEmail(current_user, email)
    return r

@router.put("/updatePreferences",response_model=bool)
async def updateUserSettings(preferences: UserPreferences, current_user: Annotated[UserName, Depends(get_current_user)]):
    r = await changeUserPreferences(current_user, preferences)
    return r
