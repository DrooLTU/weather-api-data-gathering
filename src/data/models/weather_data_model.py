import os
import sys
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from db import Base

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship("City", back_populates='weather_data')
    temperature = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    datetime = Column(Integer)
    readable_date = Column(DateTime)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    weather_description = Column(String(255))
    wind_deg = Column(Integer)

