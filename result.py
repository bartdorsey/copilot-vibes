from typing import Generic, TypeVar, Optional, Union, Type
from fastapi import HTTPException, status

T = TypeVar("T")


class Result(Generic[T]):
    """Represents the result of an operation that can succeed or fail."""

    def __init__(
        self,
        value: Optional[T] = None,
        exception: Optional[Exception] = None,
    ):
        self.value = value
        self.exception = exception

    @property
    def is_ok(self) -> bool:
        return self.exception is None

    @property
    def is_err(self) -> bool:
        return not self.is_ok

    @property
    def error(self) -> Optional[str]:
        """Get the error message from the exception"""
        if self.exception:
            return str(self.exception)
        return None

    @property
    def error_type(self) -> Optional[str]:
        """Get the exception type name for error handling"""
        if self.exception:
            return type(self.exception).__name__
        return None

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def err(cls, exception: Union[Exception, str]) -> "Result[T]":
        # Allow passing a string for convenience (wraps it in Exception)
        if isinstance(exception, str):
            exception = Exception(exception)
        return cls(exception=exception)

    def is_exception_type(self, exception_class: Type[Exception]) -> bool:
        """Check if the stored exception is of a specific type"""
        return isinstance(self.exception, exception_class)

    def as_http_error(self) -> HTTPException:
        """
        Convert the result error to an appropriate HTTP exception
        based on exception type
        """
        from exceptions import (
            EntityNotFoundError,
            IntegrityConstraintError,
            DatabaseError,
        )

        if not self.is_err:
            raise ValueError("Cannot convert a success result to an error")

        # Handle the case when exception is None but is_err is True
        if self.exception is None:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown error occurred",
            )

        # Handle specific exception types
        if self.is_exception_type(EntityNotFoundError):
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=self.error
            )
        elif self.is_exception_type(IntegrityConstraintError):
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=self.error
            )
        elif self.is_exception_type(DatabaseError):
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=self.error,
            )
        else:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {self.error}",
            )
