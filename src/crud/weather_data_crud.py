import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from sqlalchemy.orm import Session
from schemas.weather_data_schema import WeatherDataSchema

def get_weather_data(db: Session, weatherData: int) -> WeatherDataSchema:

    return db.query(WeatherDataSchema).filter(WeatherDataSchema.id == weatherData).first()



def get_weather_datas(db: Session, skip: int = 0, limit: int = 100) -> list[WeatherDataSchema]:
    return db.query(WeatherDataSchema).offset(skip).limit(limit).all()


def create_weather_data(db: Session, weatherData: WeatherDataSchema) -> WeatherDataSchema:
    db_weatherData = WeatherDataSchema(**weatherData.model_dump())
    db.add(db_weatherData)
    db.commit()
    db.refresh(db_weatherData)
    return db_weatherData