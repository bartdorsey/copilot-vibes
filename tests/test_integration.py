import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI

from main import lifespan
from result import Result


class TestLifespanEvent:
    @pytest.mark.asyncio
    async def test_lifespan_success(self):
        """Test successful lifespan execution"""
        # Setup
        mock_db = MagicMock()

        def mock_get_db():
            return iter([mock_db])

        mock_app = FastAPI()
        mock_result = Result.ok(None)

        # Execute
        with patch("crud.create_sample_data", return_value=mock_result):
            with patch("main.get_db", mock_get_db):
                async with lifespan(mock_app):
                    # This represents the main application running
                    pass

        # Assert
        mock_db.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_with_error(self):
        """Test lifespan with sample data error"""
        mock_db = MagicMock()

        def mock_get_db():
            return iter([mock_db])

        mock_app = FastAPI()
        mock_error_result = Result.err("Sample data error")
        mock_error_result = Result.err("Sample data error")

        # Execute - should continue despite error
        with patch("crud.create_sample_data", return_value=mock_error_result):
            with patch("main.get_db", mock_get_db):
                async with lifespan(mock_app):
                    # This represents the main application running
                    pass

        # Assert
        mock_db.close.assert_called_once()
