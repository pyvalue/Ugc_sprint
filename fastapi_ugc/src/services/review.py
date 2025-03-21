from functools import lru_cache

from bson import ObjectId

from settings import settings
from src.services.mongo_base import MongoServiceBase
from src.services.mongo_db import mongo_client


class ReviewService(MongoServiceBase):
    async def patch_one(self, id_: str, like: bool):
        await self.collection.update_one({'_id': ObjectId(id_)}, {'$push': {'likes': like}})


@lru_cache(maxsize=None)
def get_reviews_service():
    client = mongo_client
    db_name = client[settings.mongodb_name]
    collection_name = db_name[settings.mongodb_collection_reviews]
    return ReviewService(collection_name)
