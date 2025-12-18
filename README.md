# 🚀 Prompt-Powered Kickstart: Building High-Performance APIs with FastAPI & PostgreSQL

**A Beginner’s Toolkit for Modern Python Backend Development**
**Capstone Project: Beginner’s Toolkit with GenAI**

---

## 1. 🎯 Title & Objective

**Technology Chosen:** FastAPI (Python Framework) & PostgreSQL (Relational Database)  

**Objective:** To provide a streamlined, crash-course guide for developers to build a high-performance REST API using FastAPI. This toolkit focuses on the "hard parts" often skipped in basic tutorials: connecting to a real PostgreSQL database, handling authentication errors, and validating data with Pydantic.

**Why this stack?** FastAPI is rapidly replacing older frameworks like Flask due to its speed (built on Starlette) and developer experience (automatic documentation). When combined with PostgreSQL and SQLAlchemy, it creates a production-ready backend stack that is type-safe and scalable.

---

## 2. 📍 Quick Summary of the Technology

* **FastAPI:** A modern web framework for building APIs with Python 3.8+ based on standard Python type hints. It automates data validation and generates interactive API documentation (Swagger UI).
* **PostgreSQL:** An advanced, open-source object-relational database system known for reliability and robustness.
* **SQLAlchemy:** The Python SQL toolkit and Object Relational Mapper (ORM) that allows us to interact with the database using Python classes instead of raw SQL.

**Real-World Use Case:** Companies like **Netflix** and **Uber** use FastAPI for internal machine learning services and crisis management dashboards where speed and type safety are critical.

---

## 3. 💻 System Requirements

To follow this toolkit, ensure you have the following installed:

* **Operating System:** Linux (Ubuntu/WSL), macOS, or Windows.
* **Runtime:** Python 3.10 or higher.
* **Database:** PostgreSQL (v14 or newer).
* **IDE:** VS Code (recommended) or PyCharm.
* **Terminal:** Bash, Zsh, or PowerShell.

---

## 4. 🛠️ Installation & Setup Instructions

### Step 1: Project Environment
Create a clean workspace to avoid dependency conflicts.

```bash
# 1. Create a project folder
mkdir fastapi-starter
cd fastapi-starter

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the environment
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### Step 2: Install Dependencies
We need the web server (Uvicorn), the framework (FastAPI), and database adapters.

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary
```

### Step 3: Database Configuration (The Critical Step)
Many beginners fail here because they try to connect as a system user that doesn't exist in the database. We will create a dedicated user.

1.  **Switch to the Postgres system user:**
    ```bash
    sudo -u postgres psql
    ```

2.  **Run these SQL commands inside the shell:**
    ```sql
    -- Create a user with a secure password
    CREATE USER myapiuser WITH SUPERUSER PASSWORD 'securepassword123';

    -- Create the specific database for our app
    CREATE DATABASE fastapidb;

    -- Exit the shell
    \q
    ```

---

## 5. 📝 Minimal Working Example

This example demonstrates a complete API that saves "Users" to the database. It handles database connections, creates tables automatically, and validates inputs.

**File:** `main.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 1. DATABASE CONFIGURATION ---
# Connection string format: postgresql://user:password@host/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://myapiuser:securepassword123@localhost/fastapidb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. DATABASE MODEL (Table) ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# --- 3. PYDANTIC MODEL (Data Validation) ---
class UserSchema(BaseModel):
    username: str
    email: str
    is_active: bool = True

# --- 4. API ENDPOINTS ---
app = FastAPI()

@app.post("/users/")
def create_user(user: UserSchema):
    db = SessionLocal()
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Save to DB
    new_user = User(username=user.username, email=user.email, is_active=user.is_active)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return {"message": "User created successfully", "data": new_user}

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Toolkit!"}
```

### How to Run
```bash
uvicorn main:app --reload --port 8000
```

### Expected Output
Navigate to `http://127.0.0.1:8000/docs` in your browser.
1.  Open the **POST /users/** section.
2.  Click **Try it out**.
3.  Enter a JSON body and click **Execute**.
4.  You should receive a `200 OK` response with the created user data.

---

## 6. 🧠 AI Prompt Journal

This toolkit was developed by iteratively prompting Generative AI to resolve real-world integration errors. Below is a log of the prompts used to debug specific issues during the build process.

| **Prompt Used** | **Context & Problem** | **AI Response Summary & Evaluation** |
| :--- | :--- | :--- |
| *"FastAPI createdb error: connection to server on socket failed: FATAL: role 'aaronrashid' does not exist"* | **Context:** Initial database setup. <br>**Problem:** `createdb` command failed in terminal. | **AI Insight:** The AI explained that Postgres defaults to the OS username. It suggested using `sudo -u postgres createuser` to bridge the gap. <br>**Helpfulness:** ⭐⭐⭐⭐⭐ (Crucial for Linux setup). |
| *"psycopg2.OperationalError: FATAL: password authentication failed for user 'postgres'"* | **Context:** Running the Python app. <br>**Problem:** App crashed on startup. | **AI Insight:** The AI identified that while `psql` uses peer auth (no password), `localhost` connections require a password. It guided me to use `ALTER USER` to set a password. <br>**Helpfulness:** ⭐⭐⭐⭐⭐ (Solved the connection refused error). |
| *"INFO: 127.0.0.1 - POST /users?Content-Type=application/json 422 Unprocessable Entity"* | **Context:** Testing API with cURL. <br>**Problem:** Data wasn't saving; API returned validation errors. | **AI Insight:** The AI noticed I was passing `Content-Type` as a URL parameter instead of a Header. It corrected my cURL syntax. <br>**Helpfulness:** ⭐⭐⭐⭐ (Saved hours of debugging headers). |

---

## 7. ⚠️ Common Issues & Fixes

If you run into trouble, check these common pitfalls encountered during the creation of this toolkit:

### ❌ Error: `FATAL: database "fastapidb" does not exist`
* **Cause:** SQLAlchemy (the Python library) can create tables, but it cannot create the database itself.
* **Fix:** You must create the database via the terminal before running the app:
    ```bash
    createdb fastapidb
    ```

### ❌ Error: `422 Unprocessable Entity`
* **Cause:** Your request body does not match the Pydantic schema (e.g., sending a string for a boolean) OR you forgot the JSON header.
* **Fix:** Ensure your request includes the header `Content-Type: application/json`. If using Postman, select "Body" -> "Raw" -> "JSON".

### ❌ Error: `could not change directory to "/home/user": Permission denied`
* **Cause:** Running `sudo -u postgres` while inside a user-protected directory.
* **Fix:** This is a harmless warning. The command usually still works. To silence it, change directory to `/tmp` before running Postgres commands.

---

## 8. 📚 References

* [FastAPI Official Documentation](https://fastapi.tiangolo.com/) - The gold standard for modern API docs.
* [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html) - Deep dive into database models.
* [PostgreSQL Downloads](https://www.postgresql.org/download/) - Official database binaries.