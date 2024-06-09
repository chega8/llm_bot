from src.clients.mongo import MongoDBManager
from src.conf import settings


def get_mongo():
    mongodb_manager = MongoDBManager(host=settings.mongo.host, port=settings.mongo.port)
    return mongodb_manager
