from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional
from datetime import datetime

app = FastAPI(title="Example 7: Dependencies")

# ===== SIMPLE DEPENDENCIES =====

def get_current_time():
    """
    A simple dependency that provides current time.
    """
    return datetime.now()

def get_user_agent(user_agent: Optional[str] = None):
    """
    Dependency that extracts user agent from headers.
    (In real app, you'd use Header())
    """
    return user_agent or "Unknown"

@app.get("/time")
def show_time(current_time: datetime = Depends(get_current_time)):
    """
    The dependency is called automatically!
    """
    return {
        "current_time": current_time,
        "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

# ===== AUTHENTICATION DEPENDENCY =====

def verify_token(token: Optional[str] = None):
    """
    Simulates token verification.
    In real app, you'd check against database.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required"
        )
    if token != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"user_id": 123, "username": "alice"}

@app.get("/public")
def public_endpoint():
    """
    No authentication required.
    """
    return {"message": "This is public"}

@app.get("/protected")
def protected_endpoint(user: dict = Depends(verify_token)):
    """
    Requires authentication.
    Try: /protected (ERROR - no token)
    Try: /protected?token=wrong (ERROR - invalid token)
    Try: /protected?token=secret-token (SUCCESS)
    """
    return {
        "message": "This is protected",
        "user": user
    }

# ===== CHAINED DEPENDENCIES =====

def get_database():
    """
    Simulates database connection.
    """
    print("📦 Opening database connection")
    db = {"connected": True, "data": [1, 2, 3]}
    try:
        yield db  # Give it to the endpoint
    finally:
        print("🔒 Closing database connection")

def get_current_user(db: dict = Depends(get_database), token: Optional[str] = None):
    """
    This dependency DEPENDS on get_database!
    Chain: get_database → get_current_user → endpoint
    """
    if not token:
        return None
    # Simulate user lookup in database
    return {"id": 1, "username": "alice", "token": token}

@app.get("/me")
def get_my_profile(
    current_user: Optional[dict] = Depends(get_current_user),
    db: dict = Depends(get_database)
):
    """
    Uses chained dependencies.
    Try: /me
    Try: /me?token=abc123
    
    Check your terminal - you'll see database connection messages!
    """
    if not current_user:
        return {"message": "Not logged in", "db_connected": db["connected"]}
    return {
        "message": "Your profile",
        "user": current_user,
        "db_connected": db["connected"]
    }

# ===== REUSABLE PAGINATION =====

def pagination(skip: int = 0, limit: int = 10):
    """
    Reusable pagination dependency.
    """
    return {"skip": skip, "limit": limit}

@app.get("/items")
def get_items(page: dict = Depends(pagination)):
    """
    Uses pagination dependency.
    Try: /items
    Try: /items?skip=10&limit=5
    """
    fake_items = [f"Item {i}" for i in range(100)]
    start = page["skip"]
    end = start + page["limit"]
    return {
        "items": fake_items[start:end],
        "pagination": page
    }

@app.get("/users")
def get_users(page: dict = Depends(pagination)):
    """
    Same pagination dependency, different endpoint!
    """
    fake_users = [f"User {i}" for i in range(50)]
    start = page["skip"]
    end = start + page["limit"]
    return {
        "users": fake_users[start:end],
        "pagination": page
    }