from typing import List, Optional

from src.models.base import Created, Paginated


class ReviewLike(Created):
    user_id: str
    review_id: str
    like: bool


class ReviewMovie(Created):
    film_id: str
    user_id: str
    text: str


class ReviewResponse(ReviewMovie):
    id: str


class ReviewWithLikes(ReviewResponse):
    likes: Optional[List[bool]]


class ReviewWithLikesList(Paginated):
    data: List[ReviewWithLikes]
