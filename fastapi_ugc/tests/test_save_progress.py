import json
from time import sleep
from settings import settings
import requests
from datetime import datetime, timedelta
from jose import jwt

from kafka import KafkaProducer, KafkaConsumer

from tests.conftest import HOST, PORT, USER_ID, FILM_ID, VIEWED_FRAME, KAFKA_TEST_TOPIC, KAFKA_PORT, KAFKA_HOST

data = {
    'user_id': USER_ID,
    'film_id': FILM_ID,
    'viewed_frame': VIEWED_FRAME,
    'message_time': str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
}


def test_save_movie_progress():
    payload = {'user_id': USER_ID,
               'first_name': "Тест",
               'last_name': "Тест",
               'exp': datetime.now() + timedelta(minutes=5),
               'is_admin': True,
               'login': 'test@test.ru',
               'roles': ['admin', 'subscriber']}
    token = jwt.encode(payload, settings.jwt_secret_key)
    headers = {"Content-Type": "application/json; charset=utf-8", 'Authorization': f'Bearer {token}'}
    url = f'http://{HOST}:{PORT}/api/v1/view_progress/save'
    response = requests.post(url=url,
                             json=data,
                             headers=headers
                             )
    assert response.status_code == 200


def test_send_event_to_topic(delete_test_topic):
    """Проверка отправки события в Kafka"""

    producer = KafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')
    producer.send(
        key=f'{data["user_id"]}:{data["film_id"]}'.encode('utf-8'),
        topic=KAFKA_TEST_TOPIC,
        value=json.dumps(data).encode('utf-8'),
    )
    sleep(1)
    consumer = KafkaConsumer(
        KAFKA_TEST_TOPIC,
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        auto_offset_reset='earliest',
        group_id='echo-messages-to-stdout',
    )

    kafka_data = next(consumer)
    assert kafka_data[0] == KAFKA_TEST_TOPIC
    kafka_data_value = json.loads(kafka_data.value.decode('utf-8'))
    for field_name, field_value in kafka_data_value.items():
        assert data[field_name] == field_value
