from pydantic import BaseModel


class QueryParams(BaseModel):
    film_id: str
    user_id: str
    viewed_frame: int
