from engine import Engine
from models import Comment
from odmantic import ObjectId

async def getCommentsByPostId(postId: ObjectId, limit:int = 20, page:int = 0) -> list[Comment]:
    comments = await Engine.find(Comment, Comment.post == str(postId), limit=limit, skip=page*limit)
    return comments

async def getCommentById(commentId: ObjectId) -> Comment | None:
    comment = await Engine.find_one(Comment, Comment.id == commentId)
    return comment

async def getCommentsByUser(user: str, limit:int = 20, page:int = 0) -> list[Comment]:
    comments = await Engine.find(Comment, Comment.user == user, limit=limit, skip=page*limit)
    return comments

async def createComment(comment: Comment) -> Comment:
    comment = await Engine.save(comment)
    return comment

async def updateComment(comment: Comment, username: str) -> Comment | None:
    commentdb = await Engine.find_one(Comment, Comment.id == comment.id)
    if commentdb and commentdb.user == username:
        commentdb.content = comment.content
        await Engine.save(commentdb)
        return commentdb
    return None

async def deleteComment(comment_id: ObjectId, username :str) -> bool:
    comment = await Engine.find_one(Comment, Comment.id == comment_id)
    if comment and comment.user == username:
        await Engine.remove(Comment, Comment.id == comment_id)
        return True
    return False
