import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from sqlalchemy.orm import Session
from schemas.weather_data_schema import WeatherData as WeatherDataSchema, WeatherDataCreate as WeatherDataCreateSchema
from data.models.weather_data_model import WeatherData as WeatherDataModel

def get_weather_data(db: Session, weatherData: int) -> WeatherDataSchema:
    return db.query(WeatherDataModel).filter(WeatherDataModel.id == weatherData).first()


def get_weather_data_index(db: Session, skip: int = 0, limit: int = 100) -> list[WeatherDataSchema]:
    return db.query(WeatherDataModel).offset(skip).limit(limit).all()


def create_weather_data(db: Session, weatherData: WeatherDataCreateSchema) -> WeatherDataSchema:
    db_weatherData = WeatherDataModel(**weatherData.model_dump())
    db.add(db_weatherData)
    db.commit()
    db.refresh(db_weatherData)
    return db_weatherData