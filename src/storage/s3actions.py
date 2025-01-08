from .s3conector import s3_client, endpoint
from fastapi import File


PROFILE_IMAGE_ROUTE='profile'

async def uploadImage(file: File, username):
    file_key = f"imagenes/{username}.{file.filename.split('.')[1]}"
    file_content = await file.read()
    
    s3_client.put_object(
        Bucket=PROFILE_IMAGE_ROUTE,
        Key=file_key,
        Body=file_content,
        ContentType=file.content_type
    )
    file_url = f"{endpoint}/{PROFILE_IMAGE_ROUTE}/{file_key}"
    return file_url