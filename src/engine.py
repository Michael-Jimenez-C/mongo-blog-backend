from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.environ.get('MONGO_URI')
client = AsyncIOMotorClient(uri)

Engine = AIOEngine(client, database='blogapp')
