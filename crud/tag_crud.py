from typing import Union

from sqlalchemy import update
from sqlalchemy.future import select

import models
import utils
import schemas


class TagCRUD(utils.AppCRUD):
    async def get_tags(self):
        query = await self.db.execute(select(models.Tag))
        return query.scalars().all()

    async def get_tag_by_filed(self, field: str, data: Union[str, int]):
        if hasattr(models.Tag, field):
            tag = await self.db.execute(
                select(models.Tag).where(getattr(models.Tag, field) == data)
            )
            return tag.scalars().one_or_none()
        else:
            raise AttributeError(f"Tag model has no attribute {field}")

    async def get_or_create_tag(self, name: str):
        if tag := await self.get_tag_by_filed(field="name", data=name):
            return tag

        tag_db = models.Tag(name=name)
        self.db.add(tag_db)
        await self.db.commit()
        await self.db.refresh(tag_db)
        return tag_db

    # def get_tag_by_id(self, tag_id: int):
    #     return self.db.query(models.Tag).where(models.Tag.id == tag_id).one_or_none()
    #
    # def get_tag_by_name(self, name: str):
    #     return self.db.query(models.Tag).where(models.Tag.name == name).first()

    # def update_tag(self, tag_id: int, tag: schemas.TagCreate):
    #     self.db.execute(
    #         update(models.Tag).where(models.Tag.id == tag_id).values(name=tag.name)
    #     )
    #     tag_db = self.get_tag_by_id(tag_id)
    #     self.db.commit()
    #     self.db.refresh(tag_db)
    #     return tag_db
    #
    # def delete_tag(self, tag_id: int):
    #     tag_db = self.get_tag_by_id(tag_id)
    #     if tag_db is None:
    #         return True
    #     self.db.delete(tag_db)
    #     self.db.commit()
