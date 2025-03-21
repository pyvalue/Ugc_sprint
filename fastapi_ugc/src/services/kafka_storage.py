import json
from datetime import datetime
from typing import Optional

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError

from settings import settings


class KafkaStorage:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer
        self.topic = settings.kafka_topic

    async def send_message_to_topic(self, values: dict) -> None:
        message = {
            'user_id': values.get('user_id'),
            'film_id': values.get('film_id'),
            'viewed_frame': values.get('viewed_frame'),
            'message_time': str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
        }

        try:
            await self.producer.send(
                key=f'{message["user_id"]}:{message["film_id"]}'.encode('utf-8'),
                topic=self.topic,
                value=json.dumps(message).encode('utf-8'),
            )
        except KafkaError:
            pass


kafka_producer: Optional[AIOKafkaProducer] = None


async def get_kafka_producer() -> AIOKafkaProducer:
    return kafka_producer


async def get_kafka_storage() -> KafkaStorage:
    return KafkaStorage(kafka_producer)
