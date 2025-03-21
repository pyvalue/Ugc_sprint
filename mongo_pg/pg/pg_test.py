import time

from generate import PgCollection


def list_of_liked_movies(usrs, cur):
    """ Check select time for list of liked movies for 100 users """

    all_time = 0
    results = []
    with cur:
        for i in usrs:
            start_time = time.monotonic()
            cur.execute(f"SELECT movie_id FROM likes WHERE user_id='{i}'")
            cur.fetchall()
            end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
            all_time += end_time_ms
            results.append(end_time_ms)
    print(f"Average select time for list of liked movies for 1 user - {round(all_time / len(results), 2)} ms")
    return True


def number_of_likes(mvs, cur):
    """ Check select time for number of likes for 100 movies """

    all_time = 0
    results = []
    for i in mvs:
        start_time = time.monotonic()
        cur.execute(f"SELECT COUNT(id) FROM likes WHERE movie_id='{i}'")
        cur.fetchone()
        end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += end_time_ms
        results.append(end_time_ms)
    print(f"Average select time for number of likes for 1 movie - {round(all_time / len(results), 2)} ms")
    return True


def list_of_bookmarks(usrs, cur):
    """ Check select time for list of bookmarks for 100 users """

    all_time = 0
    results = []
    with cur:
        for i in usrs:
            start_time = time.monotonic()
            cur.execute(f"SELECT movie_id FROM bookmarks WHERE user_id='{i}'")
            cur.fetchall()
            end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
            all_time += end_time_ms
            results.append(end_time_ms)
    print(f"Average select time for list of bookmarks for 1 user - {round(all_time / len(results), 2)} ms")
    return True


def avg_like(mvs, cur):
    """ Check select time for avg like for 100 movies """

    all_time = 0
    results = []
    with cur:
        for i in mvs:
            start_time = time.monotonic()
            # pipeline = [{"$match": {"movie_id": i}},
            #             {"$group": {"_id": "$movie_id",
            #                         "averageQty": {"$avg": "$like"}}}]
            # db.likes.aggregate(pipeline)
            cur.execute(f"SELECT AVG(num_like) FROM likes WHERE movie_id='{i}'")
            cur.fetchone()
            end_time_ms = round((time.monotonic() - start_time) * 1000, 2)
            all_time += end_time_ms
            results.append(end_time_ms)
    print(f"Average select time for avg like for 1 movie - {round(all_time / len(results), 2)} ms")
    return True


def insert_and_select(db, cur):
    """ Real-time data reading testing """

    print('Start test insert and select')
    with cur:
        cur.execute("SELECT COUNT(id) FROM likes")
        before_num_likes = cur.fetchone()[0]

        start_time = time.monotonic()
        idx = db.insert_like(1)
        insert_time = time.monotonic() - start_time

        start_time = time.monotonic()
        cur.execute(f"SELECT id FROM likes WHERE id='{idx}'")
        selected_like = cur.fetchone()[0]
        selected_time = time.monotonic() - start_time
        print(f'Select like with _id {selected_like}')

        cur.execute("SELECT COUNT(id) FROM likes")
        after_num_likes = cur.fetchone()[0]

        print(f'Before insert likes: {before_num_likes}\n'
              f'After insert likes: {after_num_likes}\n'
              f'Insert + Select time: {insert_time + selected_time}')
    return True


if __name__ == '__main__':
    pg = PgCollection()
    limit = 100
    selected_usr = pg.select('users', limit)
    selected_mvs = pg.select('movies', limit)

    list_of_liked_movies(selected_usr, pg.get_cursor())
    number_of_likes(selected_mvs, pg.get_cursor())
    list_of_bookmarks(selected_usr, pg.get_cursor())
    avg_like(selected_mvs, pg.get_cursor())
    insert_and_select(pg, pg.get_cursor())
