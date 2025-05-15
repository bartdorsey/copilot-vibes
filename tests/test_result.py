import pytest
from fastapi import HTTPException

from result import Result
from exceptions import (
    EntityNotFoundError,
    IntegrityConstraintError,
    DatabaseError,
)


class TestResult:
    def test_ok_result(self):
        """Test successful result creation"""
        result = Result.ok("test_value")
        assert result.is_ok is True
        assert result.is_err is False
        assert result.value == "test_value"
        assert result.error is None
        assert result.exception is None

    def test_err_result_with_exception(self):
        """Test error result with exception"""
        error = ValueError("Test error")
        result = Result.err(error)
        assert result.is_ok is False
        assert result.is_err is True
        assert result.value is None
        assert result.error == "Test error"
        assert result.exception is error

    def test_err_result_with_string(self):
        """Test error result with string"""
        result = Result.err("Test error")
        assert result.is_ok is False
        assert result.is_err is True
        assert result.value is None
        assert result.error == "Test error"
        assert isinstance(result.exception, Exception)

    def test_error_type(self):
        """Test error_type property"""
        result = Result.err(ValueError("Test error"))
        assert result.error_type == "ValueError"

    def test_is_exception_type(self):
        """Test is_exception_type method"""
        result = Result.err(ValueError("Test error"))
        assert result.is_exception_type(ValueError) is True
        assert result.is_exception_type(TypeError) is False

    def test_as_http_error_entity_not_found(self):
        """Test as_http_error with EntityNotFoundError"""
        result = Result.err(EntityNotFoundError("Entity not found"))
        http_error = result.as_http_error()
        assert isinstance(http_error, HTTPException)
        assert http_error.status_code == 404
        assert http_error.detail == "Entity not found"

    def test_as_http_error_integrity_constraint(self):
        """Test as_http_error with IntegrityConstraintError"""
        result = Result.err(IntegrityConstraintError("Constraint violated"))
        http_error = result.as_http_error()
        assert isinstance(http_error, HTTPException)
        assert http_error.status_code == 400
        assert http_error.detail == "Constraint violated"

    def test_as_http_error_database_error(self):
        """Test as_http_error with DatabaseError"""
        result = Result.err(DatabaseError("Database error"))
        http_error = result.as_http_error()
        assert isinstance(http_error, HTTPException)
        assert http_error.status_code == 500
        assert http_error.detail == "Database error"

    def test_as_http_error_generic_exception(self):
        """Test as_http_error with generic exception"""
        result = Result.err(Exception("Unknown error"))
        http_error = result.as_http_error()
        assert isinstance(http_error, HTTPException)
        assert http_error.status_code == 500
        assert http_error.detail.startswith("Unexpected error:")

    def test_as_http_error_on_success_result(self):
        """Test as_http_error on success result raises ValueError"""
        result = Result.ok("test")
        with pytest.raises(ValueError):
            result.as_http_error()
