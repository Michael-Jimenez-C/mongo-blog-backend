from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("user/{user_id}")
def getusers(username: str):
    pass

@app.post("validate")
def validate():
    pass
