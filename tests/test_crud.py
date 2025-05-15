from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import Owner, Pet
import crud
from exceptions import (
    EntityNotFoundError,
    IntegrityConstraintError,
    DatabaseError,
)


class TestCrudOwnerOperations:
    def test_create_owner_success(self, mock_db):
        """Test successful owner creation"""
        # Setup
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh = lambda x: setattr(x, "id", 1)

        # Execute
        result = crud.create_owner(mock_db, "Test User")

        # Assert
        assert result.is_ok is True
        assert result.value is not None
        assert result.value.name == "Test User"
        assert result.value.id == 1
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_create_owner_integrity_error(self, mock_db):
        """Test owner creation with integrity error"""
        # Setup
        mock_db.add.return_value = None
        mock_db.commit.side_effect = IntegrityError(
            "stmt", "params", Exception("orig")
        )
        mock_db.rollback.return_value = None

        # Execute
        result = crud.create_owner(mock_db, "Test User")

        # Assert
        assert result.is_ok is False
        assert result.is_exception_type(IntegrityConstraintError)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.rollback.assert_called_once()

    def test_create_owner_database_error(self, mock_db):
        """Test owner creation with database error"""
        # Setup
        mock_db.add.return_value = None
        mock_db.commit.side_effect = SQLAlchemyError("Database error")
        mock_db.rollback.return_value = None

        # Execute
        result = crud.create_owner(mock_db, "Test User")

        # Assert
        assert result.is_ok is False
        assert result.is_exception_type(DatabaseError)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.rollback.assert_called_once()

    def test_get_owners_success(self, mock_db):
        """Test successful retrieval of all owners"""
        # Setup
        mock_owners = [Owner(id=1, name="User 1"), Owner(id=2, name="User 2")]
        mock_execution_result = MagicMock()
        mock_execution_result.scalars().all.return_value = mock_owners
        mock_db.execute.return_value = mock_execution_result

        # Execute
        result = crud.get_owners(mock_db)

        # Assert
        assert result.is_ok is True
        assert result.value is not None
        assert len(result.value) == 2
        assert result.value[0].name == "User 1"
        assert result.value[1].name == "User 2"

    def test_get_owners_error(self, mock_db):
        """Test error during retrieval of all owners"""
        # Setup
        mock_db.execute.side_effect = SQLAlchemyError("Database error")

        # Execute
        result = crud.get_owners(mock_db)

        # Assert
        assert result.is_ok is False
        assert result.is_exception_type(DatabaseError)

    def test_get_owner_found(self, mock_db):
        """Test successful retrieval of a specific owner"""
        # Setup
        mock_owner = Owner(id=1, name="User 1")
        mock_execution_result = MagicMock()
        mock_execution_result.scalar_one_or_none.return_value = mock_owner
        mock_db.execute.return_value = mock_execution_result

        # Execute
        result = crud.get_owner(mock_db, 1)

        # Assert
        assert result.is_ok is True
        assert result.value is not None
        assert result.value.id == 1
        assert result.value.name == "User 1"

    def test_get_owner_not_found(self, mock_db):
        """Test owner not found"""
        # Setup
        mock_execution_result = MagicMock()
        mock_execution_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_execution_result

        # Execute
        result = crud.get_owner(mock_db, 999)

        # Assert
        assert result.is_ok is False
        assert result.is_exception_type(EntityNotFoundError)


class TestCrudPetOperations:
    def test_create_pet_success(self, mock_db):
        """Test successful pet creation"""
        # Setup
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh = lambda x: setattr(x, "id", 1)

        # Execute
        result = crud.create_pet(mock_db, "Fluffy", 1)

        # Assert
        assert result.is_ok is True
        assert result.value is not None
        assert result.value.name == "Fluffy"
        assert result.value.owner_id == 1
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_get_pets_success(self, mock_db):
        """Test successful retrieval of all pets"""
        # Setup
        mock_pets = [
            Pet(id=1, name="Fluffy", owner_id=1),
            Pet(id=2, name="Spot", owner_id=2),
        ]
        mock_execution_result = MagicMock()
        mock_execution_result.scalars().all.return_value = mock_pets
        mock_db.execute.return_value = mock_execution_result

        # Execute
        result = crud.get_pets(mock_db)

        # Assert
        assert result.is_ok is True
        assert result.value is not None
        assert len(result.value) == 2
        assert result.value[0].name == "Fluffy"
        assert result.value[1].name == "Spot"


class TestSampleData:
    def test_create_sample_data_empty_db(self, mock_db):
        """Test sample data creation in empty database"""
        # Setup - database is empty
        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 0
        mock_db.execute.return_value = mock_count_result
        mock_db.commit.return_value = None
        mock_db.refresh = lambda x: setattr(x, "id", 1)

        # Execute
        result = crud.create_sample_data(mock_db)

        # Assert
        assert result.is_ok is True
        assert mock_db.add_all.call_count == 2  # Called for owners and pets

    def test_create_sample_data_populated_db(self, mock_db):
        """Test sample data creation with existing data"""
        # Setup - database already has data
        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 5  # Database has records
        mock_db.execute.return_value = mock_count_result

        # Execute
        result = crud.create_sample_data(mock_db)

        # Assert
        assert result.is_ok is True
        mock_db.add_all.assert_not_called()  # Should not add data
