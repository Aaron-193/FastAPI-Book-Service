from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI(title="Example 3: Query Parameters")


@app.get("/")
def read_root():
    return {
        "message": "Query parameter examples",
        "examples": [
            "/search?q=python",
            "/search?q=python&limit=5",
            "/items?skip=10&limit=20",
            "/filter?min_price=10&max_price=100&in_stock=true",
        ],
    }


@app.get("/search")
def search(
    q: str, limit: int = 10  # Required (no default value)  # Optional (has default)
):
    """
    q is REQUIRED
    limit is OPTIONAL (defaults to 10)

    Try: /search?q=python
    Try: /search?q=python&limit=5
    Try: /search (ERROR - q is required!)
    """
    return {
        "query": q,
        "limit": limit,
        "results": f"Searching for '{q}' with limit {limit}",
    }


@app.get("/items")
def list_items(skip: int = 0, limit: int = 10, sort_by: Optional[str] = None):
    """
    All parameters are optional here.

    Try: /items
    Try: /items?skip=5
    Try: /items?skip=5&limit=20
    Try: /items?skip=5&limit=20&sort_by=price
    """
    return {
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "message": f"Showing items {skip} to {skip + limit}",
    }


@app.get("/filter")
def filter_items(
    min_price: float = Query(0, ge=0, description="Minimum price"),
    max_price: float = Query(1000, le=10000, description="Maximum price"),
    in_stock: bool = Query(True, description="Only in-stock items?"),
    category: Optional[str] = Query(None, min_length=2, max_length=50),
):
    """
    Using Query() for advanced validation.

    Try: /filter
    Try: /filter?min_price=10&max_price=100
    Try: /filter?in_stock=false
    Try: /filter?category=electronics
    Try: /filter?min_price=-5 (ERROR - must be >= 0)
    """
    return {
        "filters": {
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock,
            "category": category,
        },
        "message": f"Filtering items: ${min_price} - ${max_price}",
    }


@app.get("/compare")
def compare_params(
    path_id: str = "default",  # Query parameter (has =)
):
    """
    This is a query parameter because it has a default value.
    Try: /compare
    Try: /compare?path_id=custom
    """
    return {"path_id": path_id, "type": "query parameter"}


@app.get("/compare/{path_id}")
def compare_path(path_id: str):
    """
    This is a path parameter (in the URL path).
    Try: /compare/123
    """
    return {"path_id": path_id, "type": "path parameter"}
