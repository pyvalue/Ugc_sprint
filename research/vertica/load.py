from datetime import datetime

import vertica_python
import time
import uuid
from faker import Faker
from random import choice, randint


connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


def gen_data(row: int, iterate: int):
    block = []
    fake = Faker()
    timestamp = fake.date_time()

    for i in range(row * iterate):
        viewed_frame = fake.random_int(min=10, max=10)

        block.append((str(uuid.uuid4()),
                      str(uuid.uuid4()),
                      str(uuid.uuid4()),
                      viewed_frame,
                      timestamp))

        if len(block) == row:
            yield block
            block = []
            timestamp = fake.date_time()


def get_user_ids(cursor):
    rows = cursor.execute("""SELECT DISTINCT user_id from views""")
    return [str(row[0]) for row in rows.iterate()]


def get_movie_ids(cursor):
    rows = cursor.execute("""SELECT DISTINCT movie_id from views""")
    return [str(row[0]) for row in rows.iterate()]


if __name__ == "__main__":
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS views (
            id UUID,
            user_id UUID,
            movie_id UUID,
            viewed_frame INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
        """)

        # Check insert time for 10 000 000
        print('start insert')
        start = time.time()

        for i in gen_data(1000, 100):
            cursor.executemany(
                """INSERT INTO views """
                """(id, user_id, movie_id, viewed_frame, timestamp) """
                """VALUES(%s, %s, %s, %s, %s)""",
                i)

        result_insert = time.time() - start
        print(f'Total time INSERT: {result_insert}')

        # Insert repeated values for aggregation queries
        user_ids = get_user_ids(cursor)
        movie_ids = get_movie_ids(cursor)

        values = [(
            choice(user_ids),
            choice(movie_ids),
            randint(100000, 999999),
            datetime.now(),
        )
            for i in range(1000)]

        cursor.executemany(
            """INSERT INTO views """
            """(user_id, movie_id, viewed_frame, timestamp) """
            """VALUES(%s, %s, %s, %s)""",
            values)
        print('Insert')
