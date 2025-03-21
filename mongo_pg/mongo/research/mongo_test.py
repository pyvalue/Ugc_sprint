import time
from generate import MngCollection


def list_of_liked_movies(usrs):
    """ Check select time for list of liked movies for 100 users """

    all_time = 0
    results = []
    for i in usrs:
        start_time = time.monotonic()
        list(db.likes.find({'user_id': i}, {'movie_id': 1, '_id': 0}))
        end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += end_time_ms
        results.append(end_time_ms)
    print(f"Average select time for list of liked movies for 1 user - {round(all_time / len(results), 2)} ms")
    return True


def number_of_likes(mvs):
    """ Check select time for number of likes for 100 movies """

    all_time = 0
    results = []
    for i in mvs:
        start_time = time.monotonic()
        db.likes.count_documents({'movie_id': i})
        end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += end_time_ms
        results.append(end_time_ms)
    print(f"Average select time for number of likes for 1 movie - {round(all_time / len(results), 2)} ms")
    return True


def list_of_bookmarks(usrs):
    """ Check select time for list of bookmarks for 100 users """

    all_time = 0
    results = []
    for i in usrs:
        start_time = time.monotonic()
        list(db.bookmarks.find({'user_id': i}, {'movie_id': 1, '_id': 0}))
        end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += end_time_ms
        results.append(end_time_ms)
    print(f"Average select time for list of bookmarks for 1 user - {round(all_time / len(results), 2)} ms")
    return True


def avg_like(mvs):
    """ Check select time for avg like for 100 movies """

    all_time = 0
    results = []
    for i in mvs:
        start_time = time.monotonic()
        pipeline = [{"$match": {"movie_id": i}},
                    {"$group": {"_id": "$movie_id",
                                "averageQty": {"$avg": "$like"}}}]
        db.likes.aggregate(pipeline)
        end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += end_time_ms
        results.append(end_time_ms)
    print(f"Average select time for avg like for 1 movie - {round(all_time / len(results), 2)} ms")
    return True


def insert_and_select(mgr):
    """ Real-time data reading testing """

    print('Start test insert and select')
    db = mgr.conn_mongo()
    like = mgr.create_data('likes')
    collection_likes = db.get_collection('likes')
    before_num_likes = collection_likes.count_documents({})

    start_time = time.monotonic()
    inserted_like = collection_likes.insert_one(like).inserted_id
    insert_time = time.monotonic() - start_time
    print(f'Insert like with _id {inserted_like}')

    start_time = time.monotonic()
    selected_like = collection_likes.find_one(
        {'user_id': like['user_id'], 'movie_id': like['movie_id']}, {'_id': 1})
    selected_time = time.monotonic() - start_time
    print(f'Select like with _id {selected_like}')

    after_num_likes = collection_likes.count_documents({})
    print(f'Before insert likes: {before_num_likes}\n'
          f'After insert likes: {after_num_likes}\n'
          f'Insert + Select time: {insert_time + selected_time}')
    return True


if __name__ == '__main__':
    mgr = MngCollection()
    db = mgr.conn_mongo()
    limit = 100
    selected_usr = [i['user_id'] for i in list(db.likes.find({}, {'user_id': 1, '_id': 0}).limit(limit))]
    selected_mvs = [i['movie_id'] for i in list(db.likes.find({}, {'movie_id': 1, '_id': 0}).limit(limit))]

    list_of_liked_movies(selected_usr)
    number_of_likes(selected_mvs)
    list_of_bookmarks(selected_usr)
    avg_like(selected_mvs)
    insert_and_select(mgr)
