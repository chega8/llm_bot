import os

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBManager:
    def __init__(self, host, port):
        self.client = AsyncIOMotorClient(host=host, port=port)

    def get_database(self, db_name: str):
        return self.client[db_name]

    def close(self):
        self.client.close()

    async def ping(self):
        await self.client.admin.command("ping")

    async def create_collection(self, db_name, collection_name):
        await self.client[db_name].create_collection(collection_name)

    async def create_db(self, db_name):
        await self.client[db_name].command("ping")
