import motor.motor_asyncio

from settings import settings

host = settings.mongodb_host
port = settings.mongodb_port


mongo_client = motor.motor_asyncio.AsyncIOMotorClient(host=host, port=port, maxPoolSize=10)
