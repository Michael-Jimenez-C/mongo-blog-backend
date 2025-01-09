from fastapi import APIRouter,File,Form, UploadFile, Depends, HTTPException
from models import User
from routers.oauth.oauth import get_current_user
from storage.s3actions import uploadImage
from utils.users_queries import changeUserImage

router = APIRouter(
    tags=["storage"]
)

@router.post("/profile")
async def uploadUserPicture(file: UploadFile = File(...),user: User = Depends(get_current_user)):
    """
    Allows users to change the profile picture
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="The specified file is not a valid image")
        file_url = await uploadImage(file, user.username)
        return {"message":"Profile picture Changed", "url":file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))