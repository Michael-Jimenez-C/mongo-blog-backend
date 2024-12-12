from models import User, UserName, UserSaved, UserReactions, Post, Comment, UserLogin, PasswordChange, ChangeEmail, ChangeUserInformation, UserPreferences
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
    user.password = hashlib.sha256(bytes(user.password,'utf-8')).hexdigest()
    user_ = None
    try:
        user_ = await Engine.save(user)
    except DuplicateKeyError:
        return False
    if user_:
        return True
    return False

async def removeUser(username:str):
    try:
        await Engine.remove(User, User.username == username)
        await Engine.remove(UserSaved, UserSaved.user == username)
        await Engine.remove(UserReactions, UserReactions.user == username)
        await Engine.remove(Post, Post.user == username)
        await Engine.remove(Comment, Comment.user == username)
        return True
    except Exception as e:
        print(e)
        return False

async def check_user(user :str, password: str) -> User | None:
    userdb = await getUserByUsername(user)
    if userdb and userdb.password == password:
        return userdb
    return None

async def changePassword(user: UserName, password: PasswordChange):
    password.old_password = hashlib.sha256(bytes(password.old_password,'utf-8')).hexdigest()
    userdb = await check_user(user.username,password.old_password)
    if not userdb:
        return False
    password.new_password = hashlib.sha256(bytes(password.new_password,'utf-8')).hexdigest()
    userdb.password = password.new_password
    await Engine.save(userdb)
    return True

async def changeEmail(user: UserName, email: ChangeEmail):
    email.password = hashlib.sha256(bytes(email.password,'utf-8')).hexdigest()
    userdb = await check_user(user.username,email.password)
    if not userdb:
        return False
    user_ = await getUserByEmail(email.email)
    if user_:
        return False
    userdb.email = email.email
    await Engine.save(userdb)
    return True

async def changeUserPreferences(user: UserName, preferences: UserPreferences):
    userdb = await getUserByUsername(user.username)
    if not userdb:
        return False
    userdb.settings = preferences
    await Engine.save(userdb)
    return True

async def changeUserInformation(user: UserName, information: ChangeUserInformation):
    userdb = await getUserByUsername(user.username)
    if not userdb:
        return False
    userdb.model_update(information)
    await Engine.save(userdb)
    return True

async def login(user: UserLogin):
    user.password = hashlib.sha256(bytes(user.password,'utf-8')).hexdigest()
    user_ = await Engine.find_one(User, (User.username == user.username) & (User.password == user.password))
    if user_:
        return {'username':user.username}
    return False
