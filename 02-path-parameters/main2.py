from fastapi import FastAPI

app = FastAPI(title="Example 2: Path Parameters")

@app.get("/")
def read_root():
    return {
        "message": "Try these URLs:",
        "examples": [
            "/users/123",
            "/users/alice",
            "/items/5/details"
        ]
    }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Path parameter with TYPE.
    Try: /users/123 ✅
    Try: /users/abc ❌ (will give error - not a number!)
    """
    return {
        "user_id": user_id,
        "type": type(user_id).__name__,
        "message": f"You requested user #{user_id}"
    }

@app.get("/users/{username}/profile")
def get_user_profile(username: str):
    """
    Path parameter as string.
    Try: /users/alice/profile
    Try: /users/bob/profile
    """
    return {
        "username": username,
        "profile_url": f"/users/{username}/profile"
    }

@app.get("/items/{item_id}/details")
def get_item_details(item_id: int):
    """
    Multiple path segments.
    Try: /items/5/details
    """
    return {
        "item_id": item_id,
        "details": f"Details for item #{item_id}"
    }

# IMPORTANT: Order matters! More specific routes FIRST
@app.get("/products/latest")
def get_latest_products():
    """
    This MUST come BEFORE /products/{product_id}
    Otherwise "latest" would be treated as a product_id!
    """
    return {"message": "Here are the latest products"}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    """
    This comes AFTER the specific route.
    """
    return {"product_id": product_id}