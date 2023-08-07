import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-force', action='store_true', help='Use this flag to force the action.', default=False)

args = parser.parse_args()

from db import DB_URL
from cities_table import create_table as create_cities_table
from weather_table import create_table as create_weather_table

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    create_cities_table(engine, args.force)
    create_weather_table(engine, args.force)

