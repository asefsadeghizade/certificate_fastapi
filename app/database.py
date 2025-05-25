import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load the DATABASE_URL from the environment
DATABASE_URL = os.environ.get("DATABASE_URL")

# Ensure it fails early if DATABASE_URL is not set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
