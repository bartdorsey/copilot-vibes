"""
Main FastAPI application for the Pet Shop API.
Provides endpoints to create and list owners and pets.
"""

import os
from fastapi import (
    FastAPI,
    Depends,
    status,
    HTTPException,
    UploadFile,
    File,
    Form,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from contextlib import asynccontextmanager
from datetime import datetime
from pydantic import BaseModel

from database import get_db, User
from schemas import PetRead, OwnerCreate, OwnerRead
import crud
from passlib.hash import bcrypt


def get_app_description() -> str:
    """Return a description for the FastAPI app."""
    return """
        ## Pet Shop API

        This API allows you to manage pet owners and their pets.
        You can create owners, add pets, and list all owners and pets.

        - **Create and list owners**
        - **Create and list pets**
        - **Relational integrity**: Pets must have a valid owner
        """


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to insert sample data on startup."""
    db = next(get_db())
    try:
        result = crud.create_sample_data(db)
        if result.is_err:
            print(f"Warning: Failed to create sample data: {result.error}")
            # Consider logging this properly with a logging framework
    except Exception as e:
        print(f"Critical startup error: {str(e)}")
    finally:
        db.close()
    yield


app = FastAPI(
    title="Pet Shop API",
    description=get_app_description(),
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Session middleware for user authentication
app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this",  # Change this in production!
    session_cookie="petshop_session",
)


@app.post(
    "/owners/",
    response_model=OwnerRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Owners"],
    summary="Create a new owner",
    response_description="The created owner object",
)
def create_owner(owner: OwnerCreate, db=Depends(get_db)):
    """
    Create a new pet owner.
    """
    result = crud.create_owner(
        db,
        name=owner.name,
        email=owner.email,
        phone=owner.phone,
        address=owner.address,
        city=owner.city,
        state=owner.state,
        zip_code=owner.zip_code,
        country=owner.country,
        date_of_birth=owner.date_of_birth,
    )
    if result.is_err:
        raise result.as_http_error()
    if result.value is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Server error: Owner creation succeeded but returned no data"
            ),
        )
    return result.value


@app.get(
    "/owners/",
    response_model=List[OwnerRead],
    tags=["Owners"],
    summary="List all owners",
    response_description="A list of all owners",
)
def list_owners(db=Depends(get_db)):
    """
    List all pet owners in the system.

    Args:
        db (Session): The database session (dependency-injected).

    Returns:
        List[OwnerRead]: A list of all owners.
    """
    result = crud.get_owners(db)
    if result.is_err:
        raise result.as_http_error()
    if result.value is None:
        # Return empty list instead of None
        return []
    return result.value


@app.post(
    "/pets/",
    response_model=PetRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Pets"],
    summary="Create a new pet",
    response_description="The created pet object",
)
async def create_pet(
    name: str = Form(...),
    owner_id: int = Form(...),
    species: str = Form(None),
    age: int = Form(None),
    breed: str = Form(None),
    color: str = Form(None),
    weight: float = Form(None),
    description: str = Form(None),
    gender: str = Form(None),
    is_vaccinated: bool = Form(None),
    birthdate: str = Form(None),
    photo: UploadFile = File(None),
    db=Depends(get_db),
):
    """
    Create a new pet for an owner, with optional photo upload and extra fields.
    """
    owner_result = crud.get_owner(db, owner_id)
    if owner_result.is_err:
        raise owner_result.as_http_error()
    if owner_result.value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with id {owner_id} not found",
        )

    photo_filename = None
    if photo:
        images_dir = os.path.join(os.path.dirname(__file__), "images")
        os.makedirs(images_dir, exist_ok=True)
        photo_filename = photo.filename or "uploaded_photo"
        file_path = os.path.join(images_dir, str(photo_filename))
        with open(file_path, "wb") as f:
            f.write(await photo.read())

    # Set date_added to now if not provided
    date_added = datetime.now().isoformat()

    pet_result = crud.create_pet(
        db,
        name,
        owner_id,
        species,
        photo_filename,
        age,
        breed,
        color,
        weight,
        description,
        gender,
        is_vaccinated,
        birthdate,
        date_added,
    )
    if pet_result.is_err:
        raise pet_result.as_http_error()
    if pet_result.value is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error: Pet creation succeeded but returned no data",
        )
    return pet_result.value


@app.get(
    "/pets/",
    response_model=List[PetRead],
    tags=["Pets"],
    summary="List all pets",
    response_description="A list of all pets",
)
def list_pets(db=Depends(get_db)):
    """
    List all pets in the system.

    Args:
        db (Session): The database session (dependency-injected).

    Returns:
        List[PetRead]: A list of all pets.
    """
    result = crud.get_pets(db)
    if result.is_err:
        raise result.as_http_error()
    if result.value is None:
        # Return empty list instead of None
        return []
    return result.value


# Serve pet images
app.mount(
    "/images",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "images")),
    name="images",
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(
    login_req: LoginRequest,
    request: Request,
    db=Depends(get_db),
):
    user: User | None = (
        db.query(User).filter(User.username == login_req.username).first()
    )
    if not user or not user.verify_password(login_req.password):
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )
    # Set session
    request.session["user_id"] = user.id
    return {"message": "Login successful", "username": user.username}


class SignupRequest(BaseModel):
    username: str
    password: str


@app.post("/signup")
def signup(
    signup_req: SignupRequest,
    db=Depends(get_db),
):
    # Check if username already exists
    existing = (
        db.query(User).filter(User.username == signup_req.username).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    # Hash the password
    hashed_pw = bcrypt.hash(signup_req.password)
    user = User(username=signup_req.username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Signup successful", "username": user.username}
