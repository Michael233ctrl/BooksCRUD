from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from crud.base_crud import BaseCRUD


class TagCRUD(BaseCRUD):
    def __init__(self, db: AsyncSession):
        self.model = models.Tag
        super().__init__(db, self.model)

    async def get_tags(self):
        return await self._get_all_objects(self.model.books)

    async def get_or_create_tag(self, name: str):
        if tag := await self._get_object_by_field("name", name, self.model.books):
            return tag
        return await self._create({"name": name})

    async def update_tag(self, tag_id: int, tag: schemas.TagCreate):
        tag_db = await self._get_object_by_field("id", tag_id, self.model.books)
        return await self._update(tag_db, tag.dict(exclude_unset=True))

    async def delete_tag(self, tag_id: int):
        if not (
            tag_db := await self._get_object_by_field("id", tag_id, self.model.books)
        ):
            return True
        await self._delete(tag_db)
