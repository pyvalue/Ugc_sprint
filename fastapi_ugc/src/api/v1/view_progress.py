from fastapi import APIRouter, Depends

from src.auth.verification import Access
from src.models.view_progress import QueryParams
from src.services.kafka_storage import KafkaStorage, get_kafka_storage

router = APIRouter()


@router.post(
    '/save',
    description='Save view progress to kafka',
    summary='Save view progress to kafka',
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_view_progress_to_kafka(
    save_view_progress_to_kafka_params: QueryParams,
    kafka_storage: KafkaStorage = Depends(get_kafka_storage),
):
    await kafka_storage.send_message_to_topic(save_view_progress_to_kafka_params.dict())
