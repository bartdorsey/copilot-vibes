import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from database import Owner, Pet
from main import app, get_db
from result import Result


@pytest.fixture
def mock_db():
    """Mock database session"""
    mock = MagicMock()
    return mock


@pytest.fixture
def test_app(mock_db):
    """Test client with mocked database session"""
    app.dependency_overrides[get_db] = lambda: mock_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_owner():
    """Sample owner data"""
    return Owner(id=1, name="Test Owner")


@pytest.fixture
def test_pet(test_owner):
    """Sample pet data"""
    return Pet(id=1, name="Test Pet", owner_id=test_owner.id)


@pytest.fixture
def mock_owner_result(test_owner):
    """Successful owner result"""
    return Result.ok(test_owner)


@pytest.fixture
def mock_pet_result(test_pet):
    """Successful pet result"""
    return Result.ok(test_pet)


@pytest.fixture
def mock_error_result():
    """Error result"""
    from exceptions import DatabaseError

    return Result.err(DatabaseError("Test database error"))
