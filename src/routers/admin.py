from fastapi import APIRouter
import os

router = APIRouter(
    tags=["Admin"]
)

@router.post('/configure')
async def configure(passwd: str):
    """
    Utility endpoint to configure the database and create the necessary indexes.
    ADMIN_PSSWD must be set in the environment variables.
    """
    if os.environ.get('ADMIN_PSSWD') == passwd:
        from engine import Engine
        from models import DBMODEL
        await Engine.configure_database(DBMODEL,update_existing_indexes=True)
