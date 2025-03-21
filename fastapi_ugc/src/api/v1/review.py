from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import Response

from src.auth.verification import Access
from src.models.review import ReviewMovie, ReviewResponse, ReviewWithLikesList
from src.services.review import get_reviews_service, ReviewService

router = APIRouter()


@router.post(
    '',
    description='Save review to mongo',
    summary='Save review to mongo',
    response_model=ReviewResponse,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_view_review_to_mongo(
    review_data: ReviewMovie,
    review_service: ReviewService = Depends(get_reviews_service),
):
    return await review_service.insert_one(review_data.dict())


@router.post(
    '/{id}/like',
    description='Save like for review',
    summary='Save like for review',
    response_class=Response,
    status_code=201,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_like_for_review_to_mongo(
    like: bool,
    review_service: ReviewService = Depends(get_reviews_service),
    id_: str = Path(alias='id'),
):
    return await review_service.patch_one(id_, like)


@router.get(
    '/movies/{id}',
    description='Show all movie reviews',
    summary='Show all movie reviews',
    response_model=ReviewWithLikesList,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def show_all_movie_reviews(
    id_: str = Path(alias='id'),
    review_service: ReviewService = Depends(get_reviews_service),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
):
    return await review_service.find_all_with_paging({'film_id': id_}, page, page_size)


@router.delete(
    '/{id}',
    description='Delete review',
    summary='Delete review',
    response_class=Response,
    status_code=201,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def delete_review(
    id_: str = Path(alias='id'),
    bookmarks_service: ReviewService = Depends(get_reviews_service),
):
    await bookmarks_service.delete_one(id_)
