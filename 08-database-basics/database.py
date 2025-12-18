"""
This file manages the database connection.
Think of it as the "phone line" to your database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that DATABASE_URL exists
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file!")

print(f"📡 Connecting to database...")

# ===== THE ENGINE =====
# This is like the "car" that drives data back and forth
# echo=True means it will print SQL queries (good for learning!)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True  # Verify connections before using them
)

# ===== THE SESSION FACTORY =====
# This creates "conversations" with the database
# autocommit=False: We control when to save changes
# autoflush=False: We control when to send changes to DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ===== THE BASE CLASS =====
# All our database models will inherit from this
Base = declarative_base()

# ===== DEPENDENCY FUNCTION =====
def get_db():
    """
    This is a dependency that provides a database session.
    
    How it works:
    1. Create a new session
    2. Give it to whoever needs it (yield)
    3. Close it when done (finally)
    
    Think of it like:
    - Checking out a library book (create session)
    - Reading it (use session)
    - Returning it (close session)
    """
    db = SessionLocal()
    try:
        yield db  # The endpoint uses the session here
    finally:
        db.close()  # Always close, even if there's an error
        print("🔒 Database session closed")

# ===== HELPER FUNCTIONS =====
def create_tables():
    """
    Create all tables in the database.
    Call this once at startup.
    """
    print("🏗️  Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")

def drop_tables():
    """
    Delete all tables (use carefully!)
    Useful for testing or resetting.
    """
    print("💥 Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped!")