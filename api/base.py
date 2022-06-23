from fastapi import APIRouter

from api.version1 import route_books
from api.version1 import route_users
from api.version1 import route_login

api_router = APIRouter()
api_router.include_router(route_books.router, prefix="/books", tags=["books"])
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
