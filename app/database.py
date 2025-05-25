import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Default DATABASE_URL if not set in environment
DEFAULT_DATABASE_URL = "postgresql://root:vkoCPvy3OSyZ9xE57sqF0mZU@certificate-db:5432/postgres"

# Load the DATABASE_URL from the environment or use default
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

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
