from fastapi import FastAPI
from routers.oauth import oauth
from routers import users

app = FastAPI()

app.include_router(oauth.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
