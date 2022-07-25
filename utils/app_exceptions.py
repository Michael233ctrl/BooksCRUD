from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException:
    class BookGet(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Book not found
            """
            status_code = status.HTTP_404_NOT_FOUND
            AppExceptionCase.__init__(self, status_code, context)

    class BookCreate(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Book creation failed
            """
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            AppExceptionCase.__init__(self, status_code, context)

    class BookUpdate(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Book update failed
            """
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            AppExceptionCase.__init__(self, status_code, context)

    class BookAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Book is not public and requires auth
            """
            status_code = status.HTTP_400_BAD_REQUEST
            AppExceptionCase.__init__(self, status_code, context)

    class BookRequiresAuth(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Book is not public and requires auth
            """
            status_code = status.HTTP_401_UNAUTHORIZED
            AppExceptionCase.__init__(self, status_code, context)

    class BookTagDoesNotExist(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Book and Tag relationship doesn't exist
            """
            status_code = status.HTTP_400_BAD_REQUEST
            AppExceptionCase.__init__(self, status_code, context)

    class UserGet(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User not found
            """
            status_code = status.HTTP_404_NOT_FOUND
            AppExceptionCase.__init__(self, status_code, context)

    class UserUnauthorized(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User authorize failed
            """
            status_code = status.HTTP_401_UNAUTHORIZED
            AppExceptionCase.__init__(self, status_code, context)

    class UserCreate(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User creation failed
            """
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            AppExceptionCase.__init__(self, status_code, context)


class BookGet(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Book not found
        """
        status_code = status.HTTP_404_NOT_FOUND
        AppExceptionCase.__init__(self, status_code, context)
