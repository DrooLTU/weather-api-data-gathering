import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-force', action='store_true', help='Use this flag to force the action.', default=False)

args = parser.parse_args()

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models.weather_data_model import WeatherData
from db import DB_URL


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_table(engine, force):
    insp = inspect(engine)
    if not insp.has_table("weather_data") or force:
        WeatherData.metadata.create_all(bind=engine)
        print("Weather data table created successfully.")
    else:
        print("Weather data table already exists.")

if __name__ == "__main__":
    create_table(engine, args.force)