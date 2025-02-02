from fastapi import APIRouter, Depends
from odmantic import ObjectId
from models import User, UserName, Post
from .oauth.oauth import get_current_user
from utils.posts_queries import getPostsByUser, addPost, delPost, getPosts

import os
if os.environ.get('USE_ARTICLE_S3'):
    from storage.s3actions import uploadArticle

router = APIRouter(
    tags=['Posts'],
    prefix='/posts'
)

@router.get('/posts')
async def getUserPosts(user: str, page: int = 0, limit: int = 20):
    r = await getPostsByUser(user, page, limit)
    return r

@router.get('/all')
async def getAllPosts(page: int = 0, limit: int = 20):
    r = await getPosts(page, limit)
    return r

@router.post('/add')
async def addPosts(post: Post, user: User = Depends(get_current_user)):
    if Post.user == user.username:
        if os.environ.get('USE_ARTICLE_S3'):
            url = await uploadArticle(post.content,post.title,user.username)
            post.content=url
        r = await addPost(post)
        return r
    return None

@router.delete('/delete')
async def delPosts(post_id: ObjectId, user: User = Depends(get_current_user)):
    if Post.user == user.username:
        r = await delPost(post_id)
        return r
    return None
