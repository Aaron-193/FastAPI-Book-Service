from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(title="Example 4: Request Body")

# Define data models
class User(BaseModel):
    """A simple user model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    """A product model with more fields"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = Field(None, ge=0)
    tags: list[str] = []

@app.get("/")
def read_root():
    return {
        "message": "Use POST requests to send data",
        "tip": "Go to /docs to try the interactive forms!"
    }

@app.post("/users")
def create_user(user: User):
    """
    Send a POST request with JSON body:
    {
        "username": "alice",
        "email": "alice@example.com",
        "age": 25,
        "is_active": true
    }
    """
    return {
        "message": "User created!",
        "user": user,
        "received_at": datetime.now()
    }

@app.post("/products")
def create_product(product: Product):
    """
    Send a POST request with JSON body:
    {
        "name": "Laptop",
        "description": "A nice laptop",
        "price": 999.99,
        "tax": 50,
        "tags": ["electronics", "computers"]
    }
    """
    total_price = product.price + (product.tax or 0)
    return {
        "message": "Product created!",
        "product": product,
        "total_price": total_price
    }

@app.post("/mixed")
def mixed_parameters(
    user_id: int,  # Path parameter
    user: User,  # Request body
    token: str = "default-token"  # Query parameter
):
    """
    Mix path, query, and body parameters!
    
    URL: POST /mixed/123?token=abc
    Body: {"username": "alice", "email": "alice@example.com"}
    """
    return {
        "user_id": user_id,
        "user": user,
        "token": token
    }

@app.post("/simple")
def simple_body(
    name: str = Body(...),
    age: int = Body(...)
):
    """
    Simple body parameters without a model.
    Body: {"name": "Alice", "age": 25}
    """
    return {"name": name, "age": age}