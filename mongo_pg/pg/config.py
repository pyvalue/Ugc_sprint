from pydantic import BaseSettings, Field


class PgConfig(BaseSettings):
    """ PG settings """
    host: str = Field('0.0.0.0')
    port: int = Field(5432)
    db: str = Field('movie_db')
    user: str = Field('app')
    password: str = Field('123qwe')
    batch_size: int = Field(1000)
    user_count: int = Field(1000)
    movie_count: int = Field(100000)
    doc_count: int = Field(100000)


class BaseConfig(BaseSettings):
    db: PgConfig = PgConfig()


configs = BaseConfig()
