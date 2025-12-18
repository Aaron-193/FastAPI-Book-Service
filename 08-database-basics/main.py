"""
This is where everything connects!
We use the database and models to create a working API.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Import our database stuff
from database import get_db, create_tables, engine, Base
import models

# ===== CREATE TABLES AT STARTUP =====
# This runs when the app starts
print("\n" + "="*50)
print("🚀 Starting FastAPI application...")
print("="*50 + "\n")

# Create all tables
Base.metadata.create_all(bind=engine)

# ===== CREATE FASTAPI APP =====
app = FastAPI(
    title="Example 8: Database Basics",
    description="Learning how to use PostgreSQL with FastAPI",
    version="1.0.0"
)

# ===== PYDANTIC SCHEMAS =====
# These define the "shape" of data in API requests/responses

class UserBase(BaseModel):
    """Base schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str | None = Field(None, max_length=100)
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating a user (what the client sends)"""
    pass

class UserResponse(UserBase):
    """Schema for returning user data (what we send back)"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy models to work

# ===== API ENDPOINTS =====

@app.get("/")
def read_root():
    """Welcome endpoint with usage instructions"""
    return {
        "message": "Database Basics Example",
        "endpoints": {
            "create_user": "POST /users",
            "get_all_users": "GET /users",
            "get_user": "GET /users/{user_id}",
            "get_by_username": "GET /users/username/{username}",
            "update_user": "PUT /users/{user_id}",
            "delete_user": "DELETE /users/{user_id}"
        },
        "docs": "/docs"
    }

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    This is where the magic happens:
    1. Check if user already exists
    2. Create new user object
    3. Add to database session
    4. Commit (save) to database
    5. Refresh to get generated ID
    6. Return the user
    """
    
    print(f"\n📝 Creating user: {user.username}")
    
    # Check if username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
    
    if existing_user:
        print(f"❌ Username '{user.username}' already exists!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user.username}' is already taken"
        )
    
    # Check if email already exists
    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    if existing_email:
        print(f"❌ Email '{user.email}' already exists!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user.email}' is already registered"
        )
    
    # Create new user instance
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active
    )
    
    # Add to session (prepares to save)
    db.add(db_user)
    print(f"➕ Added to session")
    
    # Commit (actually save to database)
    db.commit()
    print(f"💾 Committed to database")
    
    # Refresh (get the new ID from database)
    db.refresh(db_user)
    print(f"✅ User created with ID: {db_user.id}")
    
    return db_user

@app.get("/users", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all users with pagination.
    
    Query breakdown:
    - db.query(models.User) → Start a query for User table
    - .offset(skip) → Skip N records
    - .limit(limit) → Return max N records
    - .all() → Execute and return all results
    """
    
    print(f"\n📖 Getting users (skip={skip}, limit={limit})")
    
    users = db.query(models.User)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    print(f"✅ Found {len(users)} users")
    
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a single user by ID.
    
    Query breakdown:
    - db.query(models.User) → Start query
    - .filter(models.User.id == user_id) → WHERE id = user_id
    - .first() → Get first result (or None)
    """
    
    print(f"\n🔍 Looking for user ID: {user_id}")
    
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    
    if user is None:
        print(f"❌ User {user_id} not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    print(f"✅ Found user: {user.username}")
    return user

@app.get("/users/username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a user by username.
    Shows how to filter by different fields.
    """
    
    print(f"\n🔍 Looking for username: {username}")
    
    user = db.query(models.User).filter(
        models.User.username == username
    ).first()
    
    if user is None:
        print(f"❌ Username '{username}' not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found"
        )
    
    print(f"✅ Found user: {user.username} (ID: {user.id})")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing user.
    
    Steps:
    1. Find the user
    2. Update fields
    3. Commit changes
    4. Return updated user
    """
    
    print(f"\n✏️  Updating user ID: {user_id}")
    
    # Find user
    db_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    
    if db_user is None:
        print(f"❌ User {user_id} not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Update fields
    db_user.username = user_update.username
    db_user.email = user_update.email
    db_user.full_name = user_update.full_name
    db_user.is_active = user_update.is_active
    
    # Commit changes
    db.commit()
    db.refresh(db_user)
    
    print(f"✅ User updated successfully")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user permanently.
    
    Steps:
    1. Find the user
    2. Delete from session
    3. Commit
    """
    
    print(f"\n🗑️  Deleting user ID: {user_id}")
    
    # Find user
    db_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    
    if db_user is None:
        print(f"❌ User {user_id} not found!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Delete
    db.delete(db_user)
    db.commit()
    
    print(f"✅ User deleted successfully")
    return None

# ===== UTILITY ENDPOINTS =====

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Get database statistics.
    Shows how to do aggregations.
    """
    
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(
        models.User.is_active == True
    ).count()
    inactive_users = total_users - active_users
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    }

@app.post("/reset-database")
def reset_database(db: Session = Depends(get_db)):
    """
    ⚠️ DANGER: Deletes all users!
    Useful for testing.
    """
    
    print("\n⚠️  RESETTING DATABASE...")
    
    deleted = db.query(models.User).delete()
    db.commit()
    
    print(f"💥 Deleted {deleted} users")
    
    return {
        "message": f"Database reset. Deleted {deleted} users.",
        "warning": "All data has been removed!"
    }