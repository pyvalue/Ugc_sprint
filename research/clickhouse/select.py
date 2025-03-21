import time
from random import choice
from clickhouse_driver import Client
import multiprocessing

from load_online import load_clickhouse


def user_ids(client):
    rows = client.execute("""SELECT DISTINCT user_id from views.frame""")
    return [str(row[0]) for row in rows]


def movie_ids(client):
    rows = client.execute("""SELECT DISTINCT movie_id from views.frame""")
    return [str(row[0]) for row in rows]


def load():
    load_clickhouse()


def test_select():
    client = Client(host="localhost")

    # Check select time for 100
    limit = 100
    selected = [str(i[0]) for i in client.execute(f"SELECT user_id FROM views.frame LIMIT {limit}")]

    start = time.time()
    for i in selected:
        client.execute(f"SELECT * FROM views.frame WHERE user_id='{i}'")

    result_select = time.time() - start
    print(f'Total time SELECT: {result_select}')

    # Check select time for all movies with AVG viewed_frame
    start = time.time()
    client.execute("""SELECT movie_id, AVG(viewed_frame) FROM views.frame GROUP BY movie_id""")

    result_select = time.time() - start
    print(f'Time SELECT AVG viewed_frame: {result_select}')

    # Check select time for MAX viewed_frame for user and movie
    user_id = choice(user_ids(client))
    rows = client.execute(f"SELECT DISTINCT movie_id from views.frame WHERE user_id='{user_id}'")
    movies = [str(row[0]) for row in rows]
    movie_id = choice(movies)

    start = time.time()
    client.execute(f"SELECT MAX(viewed_frame) FROM views.frame WHERE user_id='{user_id}' AND movie_id='{movie_id}'")
    result_select = time.time() - start
    print(
        f'Time SELECT MAX viewed_frame for particular user amd movie: {result_select}')

    # Check select time for all movies with counted watching users
    start = time.time()
    client.execute("""SELECT movie_id, COUNT(DISTINCT user_id) FROM views.frame GROUP BY movie_id
                          ORDER BY COUNT(DISTINCT user_id)""")

    result_select = time.time() - start
    print(f'Time SELECT COUNT movies: {result_select}')

    # Check select time for all counted movies for particular user
    user_id = choice(user_ids(client))

    start = time.time()
    client.execute(f"SELECT COUNT(DISTINCT movie_id) FROM views.frame WHERE user_id='{user_id}'")

    result_select = time.time() - start
    print(f'Total time SELECT for counted movies: {result_select}')


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=load)
    p2 = multiprocessing.Process(target=test_select)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
