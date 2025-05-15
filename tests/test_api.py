from unittest.mock import patch
from fastapi import status

from exceptions import (
    EntityNotFoundError,
)
from database import Owner, Pet
from result import Result


class TestOwnerEndpoints:
    def test_create_owner_success(self, test_app, mock_owner_result):
        """Test successful owner creation"""
        # Setup
        with patch("crud.create_owner", return_value=mock_owner_result):
            # Execute
            response = test_app.post("/owners/", json={"name": "Test Owner"})

            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["name"] == "Test Owner"
            assert data["id"] == 1

    def test_create_owner_error(self, test_app, mock_error_result):
        """Test owner creation with error"""
        # Setup
        with patch("crud.create_owner", return_value=mock_error_result):
            # Execute
            response = test_app.post("/owners/", json={"name": "Test Owner"})

            # Assert
            assert (
                response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def test_list_owners_success(self, test_app):
        """Test successful listing of owners"""
        # Setup
        mock_owners = [Owner(id=1, name="User 1"), Owner(id=2, name="User 2")]
        with patch("crud.get_owners", return_value=Result.ok(mock_owners)):
            # Execute
            response = test_app.get("/owners/")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "User 1"
            assert data[1]["name"] == "User 2"

    def test_list_owners_empty(self, test_app):
        """Test listing owners with empty result"""
        # Setup
        with patch("crud.get_owners", return_value=Result.ok([])):
            # Execute
            response = test_app.get("/owners/")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == []

    def test_list_owners_null_result(self, test_app):
        """Test listing owners with null result"""
        # Setup - API should handle None by returning empty list
        with patch("crud.get_owners", return_value=Result.ok(None)):
            # Execute
            response = test_app.get("/owners/")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == []


class TestPetEndpoints:
    def test_create_pet_success(
        self, test_app, mock_pet_result, mock_owner_result
    ):
        """Test successful pet creation with photo and species"""
        # Setup
        mock_pet_result.value.species = "Dog"
        mock_pet_result.value.photo_filename = "test.jpg"
        with patch("crud.get_owner", return_value=mock_owner_result), patch(
            "crud.create_pet", return_value=mock_pet_result
        ):
            # Simulate file upload
            files = {
                "photo": ("test.jpg", b"fake image data", "image/jpeg"),
            }
            data = {
                "name": "Test Pet",
                "owner_id": 1,
                "species": "Dog",
            }
            response = test_app.post(
                "/pets/",
                data=data,
                files=files,
            )

            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["name"] == "Test Pet"
            assert data["owner_id"] == 1
            assert data["species"] == "Dog"
            assert "photo_filename" in data

    def test_create_pet_owner_not_found(self, test_app):
        """Test pet creation with non-existent owner"""
        # Setup - owner doesn't exist
        error_result = Result.err(EntityNotFoundError("Owner not found"))
        with patch("crud.get_owner", return_value=error_result):
            # Use form data, not JSON
            data = {"name": "Test Pet", "owner_id": 999}
            response = test_app.post(
                "/pets/",
                data=data,
            )

            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_pets_success(self, test_app):
        """Test successful listing of pets with photo and species"""
        # Setup
        mock_pets = [
            Pet(
                id=1,
                name="Fluffy",
                owner_id=1,
                species="Cat",
                photo_filename="fluffy.jpg",
            ),
            Pet(
                id=2,
                name="Spot",
                owner_id=2,
                species="Dog",
                photo_filename=None,
            ),
        ]
        with patch("crud.get_pets", return_value=Result.ok(mock_pets)):
            # Execute
            response = test_app.get("/pets/")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Fluffy"
            assert data[0]["species"] == "Cat"
            assert data[0]["photo_filename"] == "fluffy.jpg"
            assert data[1]["name"] == "Spot"
            assert data[1]["species"] == "Dog"
            assert data[1]["photo_filename"] is None
