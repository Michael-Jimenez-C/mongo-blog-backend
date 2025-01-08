from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers.oauth import oauth
from routers import users, admin, posts, comments
from routers.storage import S3Router


app = FastAPI()

app.include_router(oauth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(S3Router.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}