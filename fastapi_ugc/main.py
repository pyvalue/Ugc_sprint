import asyncio
import logging
import os

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from settings import settings
from src.api.v1 import view_progress, bookmark, likes, review
from src.services import kafka_storage
import logstash

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

logger = logging.getLogger(__name__)
app.include_router(view_progress.router, prefix='/api/v1/view_progress', tags=['view_progress'])
app.include_router(bookmark.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(review.router, prefix='/api/v1/reviews', tags=['reviews'])


@app.middleware("http")
async def log_middle(request: Request, call_next):
    if 'X-Request-Id' in request.headers:
        request_id = request.headers.get('X-Request-Id')
    else:
        request_id = None
    logger.info(f'request_id {request_id}')
    response = await call_next(request)
    return response


@app.on_event('startup')
async def startup():
    try:
        sentry_sdk.init(integrations=[FastApiIntegration()], dsn=os.getenv("SENTRY_SDK"), traces_sample_rate=1.0)
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}')
    kafka_storage.kafka_producer = producer
    await kafka_storage.kafka_producer.start()
    logger.setLevel(logging.INFO)
    logstash_handler = logstash.LogstashHandler('elk-logstash', 5044, version=1)
    logger.addHandler(logstash_handler)


@app.on_event('shutdown')
async def shutdown():
    await kafka_storage.kafka_producer.stop()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
