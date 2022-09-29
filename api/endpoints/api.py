from fastapi import APIRouter

from .version1 import route_books
from .version1 import route_tags
from .version1 import route_users

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_books.router, prefix="/books", tags=["books"])
api_router.include_router(route_tags.router, prefix="/tags", tags=["tags"])
