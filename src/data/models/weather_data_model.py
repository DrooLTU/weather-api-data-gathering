from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)