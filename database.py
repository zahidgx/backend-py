from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI  # Importa la URI desde config.py

client = AsyncIOMotorClient(MONGO_URI)  # Conecta el cliente
db = client["SoundAlertIA"]  # Accede a la base de datos