from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import City
from db import DB_URL


# Create the SQLAlchemy engine and session
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    # Check if the table already exists
    insp = inspect(engine)
    if not insp.has_table("cities"):
        # Create the table in the database
        City.metadata.create_all(bind=engine)
        print("Cities table created successfully.")
    else:
        print("Cities table already exists.")