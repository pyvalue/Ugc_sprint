import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    mongodb_host: str = Field(..., env='MONGODB_HOST')
    mongodb_port: int = Field(..., env='MONGODB_PORT')
    mongodb_name: str = Field(..., env='MONGODB_NAME')
    mongodb_collection_bookmarks: str = Field(..., env='MONGODB_COLLECTION_BOOKMARKS')
    mongodb_collection_likes: str = Field(..., env='MONGODB_COLLECTION_LIKES')
    mongodb_collection_reviews: str = Field(..., env='MONGODB_COLLECTION_REVIEWS')
    project_name: str = Field(..., env='PROJECT_NAME')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kafka_host: str = Field(..., env='KAFKA_HOST')
    kafka_port: str = Field(..., env='KAFKA_PORT')
    kafka_topic: str = Field(..., env='KAFKA_TOPIC')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')
    jwt_secret_key: str = Field(..., env='JWT_SECRET_KEY')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
