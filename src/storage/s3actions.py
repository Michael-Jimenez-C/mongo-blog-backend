from .s3conector import s3_client, endpoint
from fastapi import File
from PIL import Image
import io

BUCKET = 'blog'

PROFILE_IMAGE_ROUTE='pictures'

POSTS_ROUTE='articles'

async def uploadImage(file: File, username:str)->str:
    file_key = f"{PROFILE_IMAGE_ROUTE}/{username.encode().hex()}.webp"
    file_content = await file.read()
    
    original_image = Image.open(io.BytesIO(file_content))

    webp_buffer = io.BytesIO()
    original_image.save(webp_buffer, format="WEBP", optimize=True, quality=80)
    webp_buffer.seek(0)

    s3_client.put_object(
        Bucket=BUCKET,
        Key=file_key,
        Body=webp_buffer,
        ContentType='image/webp'
    )
    file_url = f"{endpoint}/{BUCKET}/{file_key}"
    return file_url



async def uploadArticle(article: str, title: str, user: str)->str:
    file_key = f"{POSTS_ROUTE}/{user}/{title}"
    article_buffer = io.BytesIO(article.encode('utf-8'))

    s3_client.put_object(
        Bucket=BUCKET,
        Key=file_key,
        Body=article_buffer,
        ContentType="text/plain"
    )
    file_url = f"{endpoint}/{BUCKET}/{file_key}"
    return file_url