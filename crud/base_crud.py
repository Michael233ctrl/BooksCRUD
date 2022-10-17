from typing import Union, TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import utils
from db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType], utils.AppCRUD):
    def __init__(self, db: AsyncSession, model):
        super().__init__(db)
        self.model = model

    async def _get_all_objects(self, opt=None):
        queryset = await self.db.execute(select(self.model).options(selectinload(opt)))
        return queryset.scalars().all()

    async def _get_object_by_field(self, field: str, data: Union[str, int], opt=None):
        if hasattr(self.model, field):
            queryset = await self.db.execute(
                select(self.model)
                .where(getattr(self.model, field) == data)
                .options(selectinload(opt))
            )
            return queryset.scalars().one_or_none()
        else:
            raise AttributeError(f"{self.model} model has no attribute {field}")

    async def __check_model_attrs(self, obj_in: dict):
        # if isinstance(obj_in, dict) and all(attr for attr in obj_in if hasattr(self.model, attr)):
        #     cleaned_data = obj_in
        if not all(attr for attr in obj_in if hasattr(self.model, attr)):
            raise AttributeError(
                f"Data doesn't correspond {self.model} model attributes"
            )

    async def _create(self, cleaned_data: dict):
        await self.__check_model_attrs(cleaned_data)
        obj_to_create = self.model(**cleaned_data)
        self.db.add(obj_to_create)
        await self.db.commit()
        await self.db.refresh(obj_to_create)
        return obj_to_create

    async def _update(self, obj_to_update, cleaned_data: dict):
        await self.__check_model_attrs(cleaned_data)
        for key, value in cleaned_data.items():
            setattr(obj_to_update, key, value)

        self.db.add(obj_to_update)
        await self.db.commit()
        await self.db.refresh(obj_to_update)
        return obj_to_update

    async def _delete(self, obj_to_delete):
        await self.db.delete(obj_to_delete)
        await self.db.commit()
