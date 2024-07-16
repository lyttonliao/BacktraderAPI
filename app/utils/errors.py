from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from typing import Any, Callable


class RecordExistsResponse(HTTPException):
    pass

class RecordNotFoundResponse(HTTPException):
    pass

class InternalErrorResponse(HTTPException):
    pass

class MethodNotAllowedResponse(HTTPException):
    pass

class BadRequestResponse(HTTPException):
    pass

class EditConflictResponse(HTTPException):
    pass

class InvalidTokenResponse(HTTPException):
    pass


def create_exception_handler(status_code: int, detail: Any) -> Callable[[Request, HTTPException], JSONResponse]:
    async def exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=status_code, content=detail)
    
    return exception_handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        RecordExistsResponse,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="the request resource already exists"
        )
    )

    app.add_exception_handler(
        RecordNotFoundResponse,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the requested resource could not be found"
        )
    )

    app.add_exception_handler(
        InternalErrorResponse,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="the server encountered a problem and could not process your request"
        )
    )

    app.add_exception_handler(
        BadRequestResponse,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bad request"
        )
    )

    app.add_exception_handler(
        MethodNotAllowedResponse,
        create_exception_handler(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="the method is not supposed for this resource"
        )
    )

    app.add_exception_handler(
        EditConflictResponse,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail="unable to update the record due to an edit conflict, please try again"
        )
    )

    app.add_exception_handler(
        InvalidTokenResponse,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="a valid token is required to access this resource"
        )
    )

