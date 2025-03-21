import pytest
from kafka.admin import KafkaAdminClient

HOST = '0.0.0.0'
PORT = '8000'
USER_ID = '1569523'
FILM_ID = '51554'
VIEWED_FRAME = 340
KAFKA_TEST_TOPIC = 'test_mviews'
KAFKA_HOST = 'kafka'
KAFKA_PORT = '9092'


@pytest.fixture
def delete_test_topic():
    """Удалить тестовый топик"""
    kafka_admin = KafkaAdminClient(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')
    yield
    kafka_admin.delete_topics(topics=[KAFKA_TEST_TOPIC])
