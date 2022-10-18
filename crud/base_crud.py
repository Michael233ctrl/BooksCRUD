from typing import Union, TypeVar, Generic, Dict, Any, List

from fastapi.encoders import jsonable_encoder
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

    async def _get_all_objects(self, opt=None) -> List[ModelType]:
        queryset = await self.db.execute(select(self.model).options(selectinload(opt)))
        return queryset.scalars().all()

    async def _get_object_by_field(
        self, field: str, data: Union[str, int], opt=None
    ) -> ModelType:
        if hasattr(self.model, field):
            queryset = await self.db.execute(
                select(self.model)
                .where(getattr(self.model, field) == data)
                .options(selectinload(opt))
            )
            return queryset.scalars().one_or_none()
        else:
            raise AttributeError(f"{self.model} model has no attribute {field}")

    async def _create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = await self.__cleaned_data(obj_in)
        obj_to_create = self.model(**obj_in_data)
        self.db.add(obj_to_create)
        await self.db.commit()
        await self.db.refresh(obj_to_create)
        return obj_to_create

    async def _update(
        self, obj_to_update: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_in_data = await self.__cleaned_data(obj_in)
        for key, value in obj_in_data.items():
            setattr(obj_to_update, key, value)

        self.db.add(obj_to_update)
        await self.db.commit()
        await self.db.refresh(obj_to_update)
        return obj_to_update

    async def _delete(self, obj_to_delete):
        await self.db.delete(obj_to_delete)
        await self.db.commit()

    async def __cleaned_data(self, obj_in: CreateSchemaType):
        encode_data = jsonable_encoder(obj_in)
        if not all(attr for attr in encode_data if hasattr(self.model, attr)):
            raise AttributeError(
                f"Data doesn't correspond {self.model} model attributes"
            )
        return encode_data
