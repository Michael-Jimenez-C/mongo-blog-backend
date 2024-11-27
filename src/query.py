from models import User, UserSaved, UserReactions, Post, Comment, UserLogin
import hashlib
from odmantic.exceptions import DuplicateKeyError
from engine import Engine

async def getUserByUsername(username: str):
    user = await Engine.find_one(User, User.username==username)
    return user

async def getUserByEmail(email: str):
    user = await Engine.find_one(User, User.email == email)
    return user

async def registerUser(user: User):

    if await getUserByUsername(user.username) or await getUserByEmail(user.email):
        return False

    user.password = hashlib.sha256(bytes(user.password,'utf-8')).hexdigest()
    user_ = None
    try:
        user_ = await Engine.save(user)
    except DuplicateKeyError:
        return False
    if user_:
        return True
    return False

async def removeUser(User):
    pass

async def login(user: UserLogin):
    user.password = hashlib.sha256(bytes(user.password,'utf-8')).hexdigest()
    user_ = await Engine.find_one(User, (User.username == user.username) & (User.password == user.password))
    if user_:
        return {'username':user.username}
    return False
