from typing import List


from src.models.base import Paginated, Created


class Bookmark(Created):
    film_id: str
    user_id: str


class BookMarkResponse(Bookmark):
    id: str


class BookMarkResponseList(Paginated):
    data: List[BookMarkResponse]
