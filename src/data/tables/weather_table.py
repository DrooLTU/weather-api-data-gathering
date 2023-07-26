from sqlalchemy import create_engine, inspect
from models import WeatherData
from db import DB_URL


# Create the SQLAlchemy engine
engine = create_engine(DB_URL)

if __name__ == "__main__":
    # Check if the table already exists
    insp = inspect(engine)
    if not insp.has_table("weather_data"):
        # Create the table in the database
        WeatherData.metadata.create_all(bind=engine)
        print("WeatherData table created successfully.")
    else:
        print("WeatherData table already exists.")