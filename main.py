from fastapi import FastAPI

from api.endpoints.api import api_router
from utils import AppExceptionCase, app_exception_handler

app = FastAPI()


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(api_router)
