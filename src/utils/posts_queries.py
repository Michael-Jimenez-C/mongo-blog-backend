from models import User, Post
from odmantic import ObjectId
from engine import Engine

async def getPostByID(post_id: ObjectId) -> Post | None:
    post = await Engine.find_one(Post, Post._id == post_id)
    return post

async def getPostsByUser(user: str, page=0, limit:int = 20) -> list[Post]:
    if page < 0 or limit < 0:
        return []
    posts = await Engine.find(Post, Post.user == user, limit=limit, skip=page*limit)
    return posts

async def getRecomendedPosts(user: str, limit:int = 20, page=0) -> list[Post]:
    posts = await Engine.find(Post, Post.user != user, limit=limit, skip=page*limit)
    return posts

async def addPost(post: Post) -> Post:
    await Engine.save(post)
    return post

async def delPost(post: ObjectId) -> bool:
    await Engine.remove(Post, Post.id == post)
    return True
