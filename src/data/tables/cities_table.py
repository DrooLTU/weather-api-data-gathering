import os
import sys
# Add the parent directory (project root) to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models.city_model import City
from db import DB_URL


# Create the SQLAlchemy engine and session
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_table(engine, force):
    insp = inspect(engine)
    if not insp.has_table("cities") or force:
        # Create the table in the database
        City.metadata.create_all(bind=engine)
        print("Cities table created successfully.")
    else:
        print("Cities table already exists.")

if __name__ == "__main__":
    create_table(engine)