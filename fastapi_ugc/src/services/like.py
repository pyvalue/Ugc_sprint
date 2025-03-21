from functools import lru_cache
from settings import settings
from src.services.mongo_base import MongoServiceBase
from src.services.mongo_db import mongo_client


class LikeService(MongoServiceBase):

    async def get_film_rate(self, film_id: str) -> dict:
        """Получить рейтинг фильма"""
        data = await self.find_all({"film_id": film_id})
        return {'film_id': film_id, 'average_rate': sum([film_like.rate for film_like in data]) / len(data)}


@lru_cache(maxsize=None)
def get_likes_service():
    client = mongo_client
    db_name = client[settings.mongodb_name]
    collection_name = db_name[settings.mongodb_collection_likes]
    return LikeService(collection_name)
