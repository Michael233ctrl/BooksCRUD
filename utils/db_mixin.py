from sqlalchemy.ext.asyncio import AsyncSession


class DBSessionMixin:
    def __init__(self, db: AsyncSession):
        self.db = db


class AppService(DBSessionMixin):
    pass


class AppCRUD(DBSessionMixin):
    pass
