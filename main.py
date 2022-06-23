from api.base import api_router
from fastapi import FastAPI
from db.session import engine
from db.base import Base

Base.metadata.create_all(engine)

# app = FastAPI()
# app.include_router(api_router)


def include_router(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    include_router(app)
    create_tables()
    return app


app = start_application()
