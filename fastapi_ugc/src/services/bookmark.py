from functools import lru_cache

from settings import settings
from src.services.mongo_base import MongoServiceBase
from src.services.mongo_db import mongo_client


class BookMarkService(MongoServiceBase):
    pass


@lru_cache(maxsize=None)
def get_bookmarks_service():
    client = mongo_client
    db_name = client[settings.mongodb_name]
    collection_name = db_name[settings.mongodb_collection_bookmarks]
    return BookMarkService(collection_name)
