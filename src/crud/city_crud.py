import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from sqlalchemy.orm import Session
from schemas.city_schema import CitySchema, CityCreateSchema

def get_city(db: Session, city: int|str) -> CitySchema:
    match city:
        case int():
            return db.query(CitySchema).filter(CitySchema.id == city).first()
        case str():
            return db.query(CitySchema).filter(CitySchema.city == city).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> list[CitySchema]:
    return db.query(CitySchema).offset(skip).limit(limit).all()


def create_city(db: Session, city: CityCreateSchema) -> CitySchema:
    db_city = CityCreateSchema(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city