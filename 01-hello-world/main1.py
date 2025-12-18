from fastapi import FastAPI

app = FastAPI(title="Example 1: Hello World")

@app.get("/")
def read_root():
    """
    The simplest possible endpoint.
    Visit: http://localhost:8000
    """
    return {"message": "Hello, World!"}

@app.get("/greet")
def greet():
    """
    Another simple endpoint.
    Visit: http://localhost:8000/greet
    """
    return {"message": "Welcome to FastAPI!"}