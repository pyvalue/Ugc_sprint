import uuid
from datetime import datetime
from random import choice, randint
from pymongo import MongoClient
from tqdm import tqdm

from config import configs


class MngCollection:
    """ Cls for operation with Mongo """

    def __init__(self):
        self.dsn = configs.db.dsn
        self.db_name = configs.db.db_name
        self.batch_size = configs.db.batch_size
        self.user_count = configs.db.user_count
        self.movie_count = configs.db.movie_count
        self.docs_count = self.user_count * 100
        self.db = self.conn_mongo()
        self.user_ids = [uuid.uuid4() for _ in range(self.user_count)]
        self.movie_ids = [uuid.uuid4() for _ in range(self.movie_count)]

    def conn_mongo(self):
        return MongoClient(self.dsn, uuidRepresentation='pythonLegacy')[self.db_name]

    def get_collection(self, collection):
        return self.db[collection]

    def get_list_collection(self):
        return self.db.list_collection_names()

    def create_data(self, collection):
        match collection:  # noqa: E999
            case 'reviews':
                return self.create_review()
            case 'likes':
                return self.create_like()
            case 'bookmarks':
                return self.create_bookmark()

    def create_like(self):
        return {'user_id': choice(self.user_ids),
                'movie_id': choice(self.movie_ids),
                'like': randint(0, 10),
                'created': datetime.now(),
                'modified': datetime.now()}

    def create_review(self):
        user_id = choice(self.user_ids)
        movie_id = choice(self.movie_ids)
        return {'user_id': user_id,
                'movie_id': movie_id,
                'review': f'Test review for {movie_id} from {user_id}',
                'created': datetime.now(),
                'modified': datetime.now()}

    def create_bookmark(self):
        return {'user_id': choice(self.user_ids),
                'movie_id': choice(self.movie_ids),
                'created': datetime.now()}


if __name__ == '__main__':
    print('Loading ..')
    db = MngCollection()
    lst_collection = db.get_list_collection()
    for c in tqdm(lst_collection, desc=str(lst_collection)):
        batch = list()
        counter = 0
        for i in tqdm(range(0, db.docs_count), desc=c):
            data = db.create_data(c)
            batch.append(data)
            if len(batch) >= db.batch_size:
                try:
                    db.get_collection(c).insert_many(batch)
                except Exception as e:
                    print(f'{e.code}: {e.message}')
                finally:
                    counter += db.batch_size
                    batch.clear()
    print('Load Complete')
