from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Example 6: Status Codes")

class Item(BaseModel):
    name: str
    price: float

# Fake database
fake_items = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Mouse", "price": 29.99},
    3: {"name": "Keyboard", "price": 79.99},
}

@app.get("/")
def read_root():
    return {
        "message": "Status code examples",
        "available_items": list(fake_items.keys())
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Returns 200 if found, 404 if not found.
    Try: /items/1 (exists)
    Try: /items/999 (doesn't exist)
    """
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return fake_items[item_id]

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    """
    Returns 201 (Created) on success.
    """
    new_id = max(fake_items.keys()) + 1
    fake_items[new_id] = item.model_dump()
    return {"id": new_id, **item.model_dump()}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """
    Returns 204 (No Content) on successful deletion.
    """
    if item_id not in fake_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    del fake_items[item_id]
    return None  # 204 returns no content

@app.get("/error-demo")
def error_demo(code: int = 400):
    """
    Demonstrates different error codes.
    Try: /error-demo?code=400
    Try: /error-demo?code=401
    Try: /error-demo?code=500
    """
    error_messages = {
        400: "Bad Request - You sent something wrong",
        401: "Unauthorized - You need to log in",
        403: "Forbidden - You don't have permission",
        404: "Not Found - This doesn't exist",
        500: "Internal Server Error - Something broke on our side",
    }
    
    raise HTTPException(
        status_code=code,
        detail=error_messages.get(code, "Unknown error")
    )

@app.post("/validate-age")
def validate_age(age: int):
    """
    Custom validation with specific error messages.
    """
    if age < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Age cannot be negative"
        )
    if age < 18:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be 18 or older"
        )
    return {"message": f"Welcome! You are {age} years old"}