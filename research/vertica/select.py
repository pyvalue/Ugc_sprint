import vertica_python
import time
import multiprocessing
from random import choice

from load_online import load_vertica


connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


def get_user_ids(cursor):
    rows = cursor.execute("""SELECT DISTINCT user_id from views""")
    return [str(row[0]) for row in rows.iterate()]


def get_movie_ids(cursor):
    rows = cursor.execute("""SELECT DISTINCT movie_id from views""")
    return [str(row[0]) for row in rows.iterate()]


def load():
    load_vertica()


def test_select():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        # Check select time for 100
        limit = 100
        selected = [str(i[0]) for i in cursor.execute(f"SELECT user_id FROM views LIMIT {limit}").iterate()]

        start = time.time()
        for i in selected:
            cursor.execute(f"SELECT * FROM views WHERE user_id='{i}'")

        result_select = time.time() - start
        print(f'Total time SELECT: {result_select}')

        # Check select time for all movies with AVG viewed_frame
        start = time.time()
        cursor.execute("""SELECT movie_id, AVG(viewed_frame) FROM views GROUP BY movie_id""")

        result_select = time.time() - start
        print(f'Time SELECT AVG viewed_frame: {result_select}')

        # Check select time for MAX viewed_frame for user and movie
        user_id = choice(get_user_ids(cursor))
        rows = cursor.execute(f"SELECT DISTINCT movie_id from views WHERE user_id='{user_id}'")
        movies = [str(row[0]) for row in rows.iterate()]
        movie_id = choice(movies)

        start = time.time()
        cursor.execute(f"SELECT MAX(viewed_frame) FROM views WHERE user_id='{user_id}' AND movie_id='{movie_id}'")
        result_select = time.time() - start
        print(
            f'Time SELECT MAX viewed_frame for particular user amd movie: {result_select}')

        # Check select time for all movies with counted watching users
        start = time.time()
        cursor.execute("""SELECT movie_id, COUNT(DISTINCT user_id) FROM views GROUP BY movie_id
                                  ORDER BY COUNT(DISTINCT user_id)""")

        result_select = time.time() - start
        print(f'Time SELECT COUNT movies: {result_select}')

        # Check select time for all counted movies for particular user
        user_id = choice(get_user_ids(cursor))

        start = time.time()
        cursor.execute(f"SELECT COUNT(DISTINCT movie_id) FROM views WHERE user_id='{user_id}'")

        result_select = time.time() - start
        print(f'Total time SELECT for counted movies: {result_select}')


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=load)
    p2 = multiprocessing.Process(target=test_select)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
