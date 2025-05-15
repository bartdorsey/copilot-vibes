class DatabaseError(Exception):
    """Base exception for database operations."""

    pass


class EntityNotFoundError(DatabaseError):
    """Raised when an entity is not found."""

    pass


class IntegrityConstraintError(DatabaseError):
    """Raised when a database constraint is violated."""

    pass
