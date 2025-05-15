from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, func
from typing import List

from database import Owner, Pet
from result import Result
from exceptions import (
    EntityNotFoundError,
    IntegrityConstraintError,
    DatabaseError,
)


# Owner operations
def create_owner(
    db: Session,
    name: str,
    email: str | None = None,
    phone: str | None = None,
    address: str | None = None,
    city: str | None = None,
    state: str | None = None,
    zip_code: str | None = None,
    country: str | None = None,
    date_of_birth: str | None = None,
) -> Result[Owner]:
    try:
        db_owner = Owner(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            date_of_birth=date_of_birth,
        )
        db.add(db_owner)
        db.commit()
        db.refresh(db_owner)
        return Result.ok(db_owner)
    except IntegrityError:
        db.rollback()
        return Result.err(
            IntegrityConstraintError(
                f"Owner with name '{name}' or email '{email}' may violate "
                f"constraints"
            )
        )
    except SQLAlchemyError as e:
        db.rollback()
        return Result.err(DatabaseError(f"Database error: {str(e)}"))


def get_owners(db: Session) -> Result[List[Owner]]:
    try:
        stmt = select(Owner)
        result = db.execute(stmt).scalars().all()
        return Result.ok(list(result))
    except SQLAlchemyError as e:
        return Result.err(DatabaseError(f"Error retrieving owners: {str(e)}"))


def get_owner(db: Session, owner_id: int) -> Result[Owner]:
    try:
        # SQLAlchemy 2.0 style
        stmt = select(Owner).where(Owner.id == owner_id)
        owner = db.execute(stmt).scalar_one_or_none()
        if not owner:
            return Result.err(
                EntityNotFoundError(f"Owner with id {owner_id} not found")
            )
        return Result.ok(owner)
    except SQLAlchemyError as e:
        return Result.err(
            DatabaseError(f"Error retrieving owner {owner_id}: {str(e)}")
        )


# Pet operations
def create_pet(
    db: Session,
    name: str,
    owner_id: int,
    species: str | None = None,
    photo_filename: str | None = None,
    age: int | None = None,
    breed: str | None = None,
    color: str | None = None,
    weight: float | None = None,
    description: str | None = None,
    gender: str | None = None,
    is_vaccinated: bool | None = None,
    birthdate: str | None = None,
    date_added: str | None = None,
) -> Result[Pet]:
    try:
        db_pet = Pet(
            name=name,
            owner_id=owner_id,
            species=species,
            photo_filename=photo_filename,
            age=age,
            breed=breed,
            color=color,
            weight=weight,
            description=description,
            gender=gender,
            is_vaccinated=is_vaccinated,
            birthdate=birthdate,
            date_added=date_added,
        )
        db.add(db_pet)
        db.commit()
        db.refresh(db_pet)
        return Result.ok(db_pet)
    except IntegrityError:
        db.rollback()
        return Result.err(
            IntegrityConstraintError(
                f"Invalid owner_id {owner_id} or constraint violation"
            )
        )
    except SQLAlchemyError as e:
        db.rollback()
        return Result.err(DatabaseError(f"Database error: {str(e)}"))


def get_pets(db: Session) -> Result[List[Pet]]:
    try:
        # SQLAlchemy 2.0 style
        stmt = select(Pet)
        result = db.execute(stmt).scalars().all()
        return Result.ok(list(result))
    except SQLAlchemyError as e:
        return Result.err(DatabaseError(f"Error retrieving pets: {str(e)}"))


# Sample data operations
def create_sample_data(db: Session) -> Result[None]:
    try:
        # Only insert if tables are empty
        # SQLAlchemy 2.0 style count
        stmt = select(func.count()).select_from(Owner)
        count = db.execute(stmt).scalar_one()

        if count == 0:
            owners = [
                Owner(
                    name="Alice Smith",
                    email="alice@example.com",
                    phone="555-1234",
                    address="123 Cat Lane",
                    city="Meowtown",
                    state="CA",
                    zip_code="90001",
                    country="USA",
                    date_of_birth="1985-04-12",
                ),
                Owner(
                    name="Bob Johnson",
                    email="bob@example.com",
                    phone="555-5678",
                    address="456 Dog Ave",
                    city="Barksville",
                    state="TX",
                    zip_code="73301",
                    country="USA",
                    date_of_birth="1978-09-23",
                ),
                Owner(
                    name="Carol Lee",
                    email="carol@example.com",
                    phone="555-8765",
                    address="789 Bird Rd",
                    city="Tweet City",
                    state="FL",
                    zip_code="33101",
                    country="USA",
                    date_of_birth="1992-12-05",
                ),
            ]
            db.add_all(owners)
            db.commit()

            from datetime import date, datetime

            pet1 = Pet(
                name="Fluffy",
                owner_id=owners[0].id,
                species="Cat",
                age=2,
                breed="Persian",
                color="White",
                weight=4.5,
                description="Playful and fluffy.",
                gender="female",
                is_vaccinated=True,
                birthdate=str(date(2023, 3, 1)),
                date_added=str(datetime.now()),
            )
            pet2 = Pet(
                name="Spot",
                owner_id=owners[1].id,
                species="Dog",
                age=5,
                breed="Dalmatian",
                color="Black & White",
                weight=20.0,
                description="Energetic and loyal.",
                gender="male",
                is_vaccinated=False,
                birthdate=str(date(2020, 7, 15)),
                date_added=str(datetime.now()),
            )
            pet3 = Pet(
                name="Whiskers",
                owner_id=owners[0].id,
                species="Cat",
                age=3,
                breed="Siamese",
                color="Cream",
                weight=3.8,
                description="Curious and vocal.",
                gender="male",
                is_vaccinated=True,
                birthdate=str(date(2022, 1, 10)),
                date_added=str(datetime.now()),
            )
            db.add_all([pet1, pet2, pet3])
            db.commit()
        return Result.ok(None)
    except SQLAlchemyError as e:
        db.rollback()
        return Result.err(
            DatabaseError(f"Error creating sample data: {str(e)}")
        )
