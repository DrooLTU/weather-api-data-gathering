import os
import sys
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from db import Base
from models.weather_data_model import WeatherData

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    # Define the relationship with WeatherData
    weather_data = relationship(WeatherData, back_populates="city")

