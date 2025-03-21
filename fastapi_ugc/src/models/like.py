from typing import List
from pydantic import BaseModel

from src.models.base import Paginated


class Like(BaseModel):
    film_id: str
    user_id: str
    rate: int


class FilmRate(BaseModel):
    film_id: str
    average_rate: float


class LikeResponseList(Paginated):
    data: List[Like]
