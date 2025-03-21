import logging
from typing import Any, Dict, Optional, List

from bson.objectid import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)


class MongoServiceBase:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def insert_one(self, data: Dict) -> Optional[Dict[str, Any]]:
        try:
            result = await self.collection.insert_one(data)
        except DuplicateKeyError:
            logger.info('duplicate key error')
            raise HTTPException(
                status_code=409,
                detail='record with the same id already exists',
            )

        inserted_id = result.inserted_id
        inserted_doc = await self.collection.find_one({'_id': inserted_id})
        logger.info('document inserted with id {0}'.format(inserted_id))
        inserted_doc_json = self.transform_to_json(inserted_doc)
        return inserted_doc_json

    async def delete_one(self, id_: str):
        filter_ = {'_id': ObjectId(id_)}
        result = await self.collection.delete_one(filter_)
        return result.deleted_count

    async def find_one(self, filter: Dict[str, str]):
        result = await self.collection.find_one(filter)
        return result

    async def find_all(self, filter: Dict[str, str]):
        result = await self.collection.find(filter).to_list(length=None)
        return result

    async def find_all_with_paging(self, filter: Dict[str, str], page: int, page_size: int):
        skip = self.make_skip(page, page_size)
        cursor_with_filter = self.collection.find(filter).skip(skip).limit(page_size)
        cursor_all_docs = self.collection.find(filter)

        filtered_results = await cursor_with_filter.to_list(length=None)
        all_results = await cursor_all_docs.to_list(length=None)
        filtered_results = self.transform_list(filtered_results)

        return {
            'data': filtered_results,
            'page': page,
            'total_count': len(all_results),
        }

    def transform_to_json(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        doc['id'] = str(doc.pop('_id'))
        return doc

    def transform_list(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Приводим ObjectID к str в каждом документе."""
        transformed_list = []
        for doc in docs:
            transformed_list.append(self.transform_to_json(doc))
        return transformed_list

    def make_skip(self, page: int, page_size: int) -> int:
        """Оффсет для запроса."""
        return page_size * (page - 1)
