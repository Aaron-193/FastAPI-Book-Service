from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="Example 5: Response Models")

# Input model (what user sends)
class UserInput(BaseModel):
    username: str
    email: EmailStr
    password: str  # User sends this

# Output model (what we return - NO PASSWORD!)
class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    # Notice: NO password field!

# Detailed user model
class UserDetailed(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: str
    login_count: int

@app.get("/")
def read_root():
    return {"message": "Response model examples"}

@app.post("/register", response_model=UserOutput)
def register_user(user: UserInput):
    """
    User sends: username, email, password
    We return: id, username, email, is_active
    Password is automatically hidden!
    """
    # Simulate saving to database
    return {
        "id": 123,
        "username": user.username,
        "email": user.email,
        "is_active": True,
        "password": user.password  # This won't appear in response!
    }

@app.get("/users/{user_id}", response_model=UserOutput)
def get_user(user_id: int):
    """
    Returns user without sensitive data.
    """
    # Simulate database fetch
    fake_user = {
        "id": user_id,
        "username": "alice",
        "email": "alice@example.com",
        "is_active": True,
        "password": "secret123",  # Won't be returned!
        "credit_card": "1234-5678"  # Won't be returned!
    }
    return fake_user

@app.get("/users/{user_id}/details", response_model=UserDetailed)
def get_user_details(user_id: int):
    """
    Returns more detailed user information.
    """
    return {
        "id": user_id,
        "username": "alice",
        "email": "alice@example.com",
        "is_active": True,
        "created_at": "2024-01-01",
        "login_count": 42
    }

@app.get("/users-list", response_model=list[UserOutput])
def get_users():
    """
    Returns a LIST of users.
    """
    fake_users = [
        {"id": 1, "username": "alice", "email": "alice@example.com", "is_active": True},
        {"id": 2, "username": "bob", "email": "bob@example.com", "is_active": False},
    ]
    return fake_users