import time
import uuid
from datetime import datetime
from random import choice, randint
from faker import Faker
from clickhouse_driver import Client


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


def get_user_ids(client):
    rows = client.execute("""SELECT DISTINCT user_id from views.frame""")
    return [str(row[0]) for row in rows]


def get_movie_ids(client):
    rows = client.execute("""SELECT DISTINCT movie_id from views.frame""")
    return [str(row[0]) for row in rows]


if __name__ == "__main__":
    client = Client(host="localhost")
    client.execute("CREATE DATABASE IF NOT EXISTS views")

    create_sql = """
    CREATE TABLE IF NOT EXISTS views.frame (
          id UUID,
          user_id UUID,
          movie_id UUID,
          viewed_frame Int32,
          timestamp DateTime('Europe/Moscow'))
          Engine=MergeTree() PARTITION BY toYYYYMMDD(timestamp) ORDER BY user_id;
    """
    client.execute(create_sql)

    # Check insert time for 100 000
    print('start insert')
    start = time.time()

    for i in gen_data(1000, 100):
        client.execute(
            "INSERT INTO views.frame (id, user_id, movie_id, viewed_frame, timestamp) VALUES",
            i,
        )

    result_insert = time.time() - start
    print(f'Total time INSERT: {result_insert}')

    # Insert repeated values for aggregation queries
    user_ids = get_user_ids(client)
    movie_ids = get_movie_ids(client)

    values = [{
        'user_id': choice(user_ids),
        'movie_id': choice(movie_ids),
        'viewed_frame': randint(100000, 999999),
        'timestamp': datetime.now(),
    }
        for i in range(1000)]

    client.execute(
        "INSERT INTO views.frame (user_id, movie_id, viewed_frame, timestamp) VALUES",
        values,
    )
    print('Insert')
