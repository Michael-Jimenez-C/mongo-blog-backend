from fastapi import FastAPI
from routers.oauth import oauth
from routers import users, admin
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

app.include_router(oauth.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
