import time
from datetime import datetime
from random import choice, randint, uniform
from clickhouse_driver import Client


def get_user_ids(client):
    rows = client.execute("""SELECT DISTINCT user_id from views.frame""")
    return [str(row[0]) for row in rows]


def get_movie_ids(client):
    rows = client.execute("""SELECT DISTINCT movie_id from views.frame""")
    return [str(row[0]) for row in rows]


def load_clickhouse():
    client = Client(host="localhost")

    # Insert repeated values for aggregation queries
    user_ids = get_user_ids(client)
    movie_ids = get_movie_ids(client)

    while True:
        values = [{'user_id': choice(user_ids),
                   'movie_id': choice(movie_ids),
                   'viewed_frame': randint(100000, 999999),
                   'timestamp': datetime.now(),
                   } for i in range(100)]

        client.execute(
            "INSERT INTO views.frame (user_id, movie_id, viewed_frame, timestamp) VALUES",
            values,
        )
        print('Insert in real time +')
        time.sleep(uniform(0.1, 0.5))
