"""
This file defines what your data looks like IN THE DATABASE.
Each class = one table.
Each attribute = one column.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base

class User(Base):
    """
    This class represents the 'users' table in the database.
    
    Each instance of this class = one row in the table.
    """
    
    # ===== TABLE NAME =====
    __tablename__ = "users"
    
    # ===== COLUMNS =====
    
    # Primary Key - unique identifier for each user
    id = Column(
        Integer,
        primary_key=True,  # This is the unique ID
        index=True,        # Create an index for faster searches
        autoincrement=True # Auto-generate: 1, 2, 3, ...
    )
    
    # Username - must be unique
    username = Column(
        String(50),        # Max 50 characters
        unique=True,       # No two users can have same username
        index=True,        # Index for faster searches
        nullable=False     # This field is REQUIRED
    )
    
    # Email - must be unique
    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )
    
    # Full name - optional
    full_name = Column(
        String(100),
        nullable=True      # This field is OPTIONAL
    )
    
    # Is the user active?
    is_active = Column(
        Boolean,
        default=True       # Default value if not specified
    )
    
    # When was this user created?
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()  # Automatically set to current time
    )
    
    # When was this user last updated?
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()  # Update automatically on changes
    )
    
    # ===== REPRESENTATION =====
    def __repr__(self):
        """
        How this object looks when you print it.
        Useful for debugging!
        """
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

# ===== EXPLANATION OF COLUMN TYPES =====
"""
Common SQLAlchemy column types:

Integer       → Whole numbers (1, 2, 3, ...)
String(N)     → Text with max length N
Text          → Long text (no limit)
Boolean       → True/False
Float         → Decimal numbers (3.14, 99.99)
Date          → Date only (2024-01-15)
DateTime      → Date + time (2024-01-15 10:30:00)
JSON          → JSON data

Common column options:

primary_key=True    → Unique identifier
unique=True         → No duplicates allowed
index=True          → Create index (faster searches)
nullable=False      → Required field
nullable=True       → Optional field
default=value       → Default value if not provided
server_default=...  → Default value set by database
autoincrement=True  → Auto-generate numbers
"""