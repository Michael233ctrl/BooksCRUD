from fastapi import HTTPException
from starlette import status


class BookNotFoundError(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "Book not found"
        super(BookNotFoundError, self).__init__(status_code=status_code, detail=detail)


class BookAlreadyExistError(HTTPException):
    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST
        detail = "Book with that title already exist"
        super(BookAlreadyExistError, self).__init__(
            status_code=status_code, detail=detail
        )


class UserNotFoundError(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "User not found"
        super(UserNotFoundError, self).__init__(status_code=status_code, detail=detail)


class UserUnauthorizedError(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Incorrect username or password"
        super(UserUnauthorizedError, self).__init__(
            status_code=status_code, detail=detail
        )
