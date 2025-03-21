from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import Response

from src.auth.verification import Access
from src.models.bookmark import BookMarkResponse, BookMarkResponseList, Bookmark
from src.services.bookmark import get_bookmarks_service, BookMarkService

router = APIRouter()


@router.post(
    '',
    description='Save bookmark to mongo',
    summary='Save bookmark to mongo',
    response_model=BookMarkResponse,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def save_view_bookmark_to_mongo(
    bookmark_data: Bookmark,
    bookmarks_service: BookMarkService = Depends(get_bookmarks_service),
):
    return await bookmarks_service.insert_one(bookmark_data.dict())


@router.delete(
    '/{id}',
    description='Delete bookmark to mongo',
    summary='Delete bookmark to mongo',
    response_class=Response,
    status_code=204,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def delete_bookmark(
    id_: str = Path(alias='id'),
    bookmarks_service: BookMarkService = Depends(get_bookmarks_service),
):
    await bookmarks_service.delete_one(id_)


@router.get(
    '/users/{id}',
    description='Show all user bookmarks',
    summary='Show all user bookmarks',
    response_model=BookMarkResponseList,
    dependencies=[Depends(Access({'admin', 'subscriber'}))],
)
async def show_all_user_bookmarks(
    id_: str = Path(alias='id'),
    bookmarks_service: BookMarkService = Depends(get_bookmarks_service),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
):
    return await bookmarks_service.find_all_with_paging({'user_id': id_}, page, page_size)
