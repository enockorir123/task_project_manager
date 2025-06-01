# project_manager/models/__init__.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Determine the project root and ensure the 'db/' directory exists
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_DIR = os.path.join(ROOT_DIR, "db")
if not os.path.isdir(DB_DIR):
    os.makedirs(DB_DIR, exist_ok=True)

# SQLite URL pointing to 'task_project_manager/db/database.db'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'database.db')}"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Set to True if you want to see SQL logs
)

# Session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models to inherit from
Base = declarative_base()
