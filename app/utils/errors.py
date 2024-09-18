from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from typing import Callable


class BacktraderAPIException(Exception):
    """base exception class"""

    def __init__(
        self, message: str = "Service is unavailable", name: str = "BacktraderAPI Error"
    ):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class RecordExistsError(BacktraderAPIException):
    """record already exists in database"""

    pass


class RecordNotFoundError(BacktraderAPIException):
    """record doesn't exist in database"""

    pass


class InternalServiceError(BacktraderAPIException):
    """request could not be processed due to an internal error"""

    pass


class MethodNotAllowedError(BacktraderAPIException):
    """invalid operation"""

    pass


class BadRequestError(BacktraderAPIException):
    """request could not be processed"""

    pass


class EditConflictError(BacktraderAPIException):
    """unable to edit this resource"""

    pass


class InvalidTokenError(BacktraderAPIException):
    """valid token must be provided"""

    pass


class ExpiredTokenError(BacktraderAPIException):
    """token has expired"""

    pass


class StatusForbiddenError(BacktraderAPIException):
    """user cannot access this resource"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, BacktraderAPIException], JSONResponse]:
    async def exception_handler(
        request: Request, exc: BacktraderAPIException
    ) -> JSONResponse:
        detail = {"message": initial_detail}

        if exc.message:
            detail["message"] = exc.message

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        return JSONResponse(status_code, content={"detail": detail["message"]})

    return exception_handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=BadRequestError,
        handler=create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST, initial_detail="bad request"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InvalidTokenError,
        handler=create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail="a valid token is required to access this resource",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=ExpiredTokenError,
        handler=create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail="the token has expired",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=StatusForbiddenError,
        handler=create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail="your account doesn't have the necessary permissions to access this resource",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=RecordExistsError,
        handler=create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail="the request resource already exists",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=RecordNotFoundError,
        handler=create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail="the requested resource could not be found",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=MethodNotAllowedError,
        handler=create_exception_handler(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            initial_detail="the method is not supposed for this resource",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=EditConflictError,
        handler=create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail="unable to update the record due to an edit conflict, please try again",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InternalServiceError,
        handler=create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail="the server encountered a problem and could not process your request",
        ),
    )
