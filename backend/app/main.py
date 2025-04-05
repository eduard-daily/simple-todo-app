# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Import necessary components from other modules within the 'app' package
from . import models, schemas # Note the '.' for relative imports
from .database import SessionLocal, engine, get_db # Import engine here

# --- Database Initialization ---
# Create database tables based on models if they don't exist
# This line tells SQLAlchemy to create all tables defined in models
# that inherit from Base (imported via 'models') using the specified engine.
# WARNING: For production, use a migration tool like Alembic instead of create_all.
print("Attempting to create database tables...")
try:
    models.Base.metadata.create_all(bind=engine)
    print("Database tables checked/created successfully.")
except Exception as e:
    print(f"Error creating database tables: {e}")
    # Depending on the error, you might want to exit or handle differently
    # For now, we'll let the app continue starting but log the error.

# --- FastAPI App Instance ---
app = FastAPI(
    title="To-Do API",
    description="A simple API to manage tasks using FastAPI and PostgreSQL.",
    version="0.2.0"
)

# --- CORS Configuration ---
origins = [
    "http://localhost:5173", # The origin of your Vite frontend dev server
    "http://127.0.0.1:5173", # Sometimes needed depending on browser/OS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints (CRUD Operations) ---

@app.post("/api/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    """
    try:
        db_task = models.Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback() # Rollback the transaction on error
        print(f"Error creating task: {e}") # Log the error server-side
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not create task: {e}")


@app.get("/api/tasks", response_model=List[schemas.TaskResponse], tags=["Tasks"])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of tasks.
    """
    try:
        tasks = db.query(models.Task).offset(skip).limit(limit).all()
        return tasks
    except Exception as e:
        print(f"Error reading tasks: {e}") # Log the error server-side
        # Don't expose internal error details to the client directly unless needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not retrieve tasks")


@app.get("/api/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single task by its ID.
    """
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return db_task
    except HTTPException:
        raise # Re-raise HTTPException (like 404) directly
    except Exception as e:
        print(f"Error reading task {task_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not retrieve task")


@app.put("/api/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task by its ID.
    """
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        raise # Re-raise HTTPException (like 404) directly
    except Exception as e:
        db.rollback()
        print(f"Error updating task {task_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update task")


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID.
    """
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        db.delete(db_task)
        db.commit()
        return None
    except HTTPException:
        raise # Re-raise HTTPException (like 404) directly
    except Exception as e:
        db.rollback()
        print(f"Error deleting task {task_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete task")


@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the To-Do API!"}
