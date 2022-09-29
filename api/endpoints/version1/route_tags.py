from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.deps import get_token, get_db
from service import TagService
from utils.service_result import handle_result
from schemas import TagCreate

router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/")
async def read_tags(db: AsyncSession = Depends(get_db)):
    return handle_result(result=await TagService(db).get_tags())


@router.put("/{tag_id}", response_model=TagCreate, status_code=status.HTTP_200_OK)
async def update_tags(tag: TagCreate, tag_id: int, db: AsyncSession = Depends(get_db)):
    return handle_result(result=TagService(db).update_tag(tag_id, tag))


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags(tag_id: int, db: AsyncSession = Depends(get_db)):
    return handle_result(result=TagService(db).delete_tag(tag_id))
