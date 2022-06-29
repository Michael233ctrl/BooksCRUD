from api.base import api_router
from fastapi import FastAPI
from db.session import engine
from db.base import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)
