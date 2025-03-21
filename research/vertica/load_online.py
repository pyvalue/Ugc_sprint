from datetime import datetime, time
from random import choice, randint, uniform
import vertica_python


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


def load_vertica():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        # Insert repeated values for aggregation queries
        user_ids = get_user_ids(cursor)
        movie_ids = get_movie_ids(cursor)

        while True:
            values = [(
                choice(user_ids),
                choice(movie_ids),
                randint(100000, 999999),
                datetime.now(),
            )
                for i in range(100)]

            cursor.executemany(
                """INSERT INTO views """
                """(user_id, movie_id, viewed_frame, timestamp) """
                """VALUES(%s, %s, %s, %s)""",
                values)
            print('Insert in real time +')
            time.sleep(uniform(0.1, 0.5))
