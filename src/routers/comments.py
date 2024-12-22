from fastapi import APIRouter, Depends
from models import User, Comment
from odmantic import ObjectId
from utils.comments_queries import createComment, deleteComment, updateComment, getCommentsByPostId, getCommentsByUser
from .oauth.oauth import get_current_user

router = APIRouter(
    tags=["Comments"],
    prefix = "/comment"
)

@router.get("/post")
async def getCommentsByPost(postId: ObjectId, limit: int = 20, page: int = 0):
    comments = await getCommentsByPostId(postId, limit, page)
    return comments

@router.get("/user")
async def getCommentsByUser_(user: str, limit: int = 20, page: int = 0):
    comments = await getCommentsByUser(user, limit, page)
    return comments

@router.post("/add")
async def addComment(comment: Comment, user: User = Depends(get_current_user)):
    if comment.user == user.username:
        comment = await createComment(comment)
        return comment
    return None

@router.put("/update")
async def updateComment_(comment: Comment, user: User = Depends(get_current_user)) -> Comment | None:
    commentUp = await updateComment(comment, user.username)
    return commentUp

@router.delete("/delete")
async def deleteComment_(comment_id: ObjectId, user: User = Depends(get_current_user)) -> bool:
    r = await deleteComment(comment_id, user.username)
    return r
