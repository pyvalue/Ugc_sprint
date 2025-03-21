from pydantic import BaseSettings, Field


class MongoConfig(BaseSettings):
    """ Mongo settings """

    dsn: str = Field('mongodb://0.0.0.0:27019, 0.0.0.0:27020')
    db_name: str = Field('ugcDB')
    batch_size: int = Field(1000)
    user_count: int = Field(1000)
    movie_count: int = Field(100000)


class BaseConfig(BaseSettings):
    db: MongoConfig = MongoConfig()


configs = BaseConfig()
