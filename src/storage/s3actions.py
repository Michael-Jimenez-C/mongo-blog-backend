from .s3conector import s3_client, endpoint
from fastapi import File
from PIL import Image
import io

PROFILE_IMAGE_ROUTE='profile'

async def uploadImage(file: File, username:str)->str:
    file_key = f"imagenes/{username.encode().hex()}.webp"
    file_content = await file.read()
    
    original_image = Image.open(io.BytesIO(file_content))

    webp_buffer = io.BytesIO()
    original_image.save(webp_buffer, format="WEBP", optimize=True, quality=80)
    webp_buffer.seek(0)

    s3_client.put_object(
        Bucket=PROFILE_IMAGE_ROUTE,
        Key=file_key,
        Body=webp_buffer,
        ContentType='image/webp'
    )
    file_url = f"{endpoint}/{PROFILE_IMAGE_ROUTE}/{file_key}"
    return file_url
