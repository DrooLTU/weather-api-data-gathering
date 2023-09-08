import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from sqlalchemy.orm import Session
from data.schemas.city_schema import City as CitySchema, CityCreate as CitySchemaCreate
from data.models.city_model import City as CityModel

def get_city(session: Session, city: int|str) -> CitySchema:
    match city:
        case int():
            return session.query(CityModel).filter(CityModel.id == city).first()
        case str():
            return session.query(CityModel).filter(CityModel.city == city).first()


def get_cities(session: Session, skip: int = 0, limit: int = 100) -> list[CitySchema]:
    return session.query(CityModel).offset(skip).limit(limit).all()


def create_city(session: Session, city: CitySchemaCreate) -> CityModel:
    session_city = CityModel(**city.model_dump())
    session.add(session_city)
    session.commit()
    session.refresh(session_city)
    return session_city