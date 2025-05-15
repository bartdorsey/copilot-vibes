from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date, datetime


# Pet schemas
class PetCreate(BaseModel):
    name: str
    owner_id: int
    species: str | None = None
    age: int | None = None
    breed: str | None = None
    color: str | None = None
    weight: float | None = None
    description: str | None = None
    gender: str | None = None  # e.g. 'male', 'female', 'unknown'
    is_vaccinated: bool | None = None
    birthdate: date | None = None
    # photo_filename is not included here


class PetRead(BaseModel):
    id: int
    name: str
    owner_id: int
    species: str | None = None
    age: int | None = None
    breed: str | None = None
    color: str | None = None
    weight: float | None = None
    description: str | None = None
    gender: str | None = None
    is_vaccinated: bool | None = None
    birthdate: date | None = None
    date_added: datetime | None = None
    photo_filename: str | None = None

    model_config = ConfigDict(from_attributes=True)


# Owner schemas
class OwnerCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
    date_of_birth: str | None = None


class OwnerRead(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
    date_of_birth: str | None = None
    pets: List["PetRead"] = []

    model_config = ConfigDict(from_attributes=True)
