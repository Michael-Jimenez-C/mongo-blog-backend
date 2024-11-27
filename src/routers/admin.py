from fastapi import APIRouter
import os

router = APIRouter(
    tags=["admin"]
)

@router.post('/configure')
async def configure(passwd: str):
    if os.environ.get('ADMIN_PSSWD') == passwd:
        from engine import Engine
        from models import DBMODEL
        await Engine.configure_database(DBMODEL,update_existing_indexes=True)
