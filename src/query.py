from pymongo import MongoClient
from models import User, UserPreferences, UserSaved, UserReactions, Post, Comment
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get('MONGO_URI')
client = MongoClient(uri)


def getUserByUsername(username: str):
    if not client:
        return None
    db = client['blogapp']
    collection = db['users']
    user = collection.find_one({'username':username})
    return user

def getUserByEmail(email: str):
    if not client:
        return None
    db = client['blogapp']
    collection = db['users']
    user = collection.find_one({'email':email})
    return user

def registerUser(user: User):
    if not client:
        return False
    db = client['blogapp']
    collection = db['users']

    if getUserByUsername(user.username) or getUserByEmail(user.email):
        return False

    user.password = hashlib.sha256(bytes(user.password,'utf-8')).hexdigest()
    userdb = dict(user)
    user_ = collection.insert_one(userdb)
    if user_.acknowledged:
        return True
    return False
