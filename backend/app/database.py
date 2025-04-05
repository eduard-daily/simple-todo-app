# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file located in the parent 'backend' directory
# Adjust the path if your .env file is elsewhere
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Consider using a default fallback for local dev if appropriate,
    # but raising an error is safer for ensuring configuration.
    raise ValueError("DATABASE_URL environment variable not set or .env file not found.")

# Create SQLAlchemy engine
# For PostgreSQL
engine = create_engine(DATABASE_URL)

# For SQLite (example, if you were using it)
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function that provides a SQLAlchemy database session per request.
    It ensures the session is always closed after the request, even if errors occur.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create database tables (optional, consider migrations like Alembic)
def init_db():
    """
    Initializes the database by creating all tables defined by models inheriting from Base.
    WARNING: Use with caution. For production, use migration tools like Alembic.
    """
    print("Attempting to create database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully (if they didn't exist).")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        