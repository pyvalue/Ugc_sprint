from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import Response
from src.auth.verification import Access
from src.models.like import Like, FilmRate, LikeResponseList
from src.services.like import get_likes_service, LikeService

router = APIRouter()


@router.post(
    '',
    description='Save personal film rate to mongo',
    summary='Save personal film rate to mongo',
    response_model=Like,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def create_like(
    like: Like,
    likes_service: LikeService = Depends(get_likes_service),
):
    return await likes_service.insert_one(like.dict())


@router.delete(
    '/{id}',
    description='Delete like from mongo',
    summary='Delete like from mongo',
    response_class=Response,
    status_code=201,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def delete_like(
    id_: str = Path(alias='id'),
    likes_service: LikeService = Depends(get_likes_service),
):
    return await likes_service.delete_one(id_)


@router.get(
    '/{film_id}/rate',
    description='Show average film rate',
    summary='Show average film rate',
    response_model=FilmRate,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def show_average_film_rate(
    film_id: str,
    likes_service: LikeService = Depends(get_likes_service),
):
    return await likes_service.get_film_rate(film_id)


@router.get(
    '/{film_id}',
    description='Show film likes',
    summary='Show film likes',
    response_model=LikeResponseList,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def get_film_likes(
    film_id: str,
    likes_service: LikeService = Depends(get_likes_service),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
):
    return await likes_service.find_all_with_paging({'film_id': film_id}, page, page_size)
