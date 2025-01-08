from fastapi import APIRouter,File, UploadFile, Depends, HTTPException
from models import User
from routers.oauth.oauth import get_current_user
from storage.s3actions import uploadImage

router = APIRouter(
    tags=["storage"]
)

@router.post("/profile")
async def uploadUserImage(file: UploadFile = File(...),user: User = Depends(get_current_user)):
    """
    Allow a user to change the profile image
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="The specified file is not a valid image")
        file_url = await uploadImage(file, user.username)
        return {"message":"Uploaded", "url":file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))