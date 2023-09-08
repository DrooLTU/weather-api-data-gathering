from datetime import datetime as dt
from pydantic import BaseModel

class WeatherDataBase(BaseModel):
    city_id: int
 
    datetime: int
    readable_date: dt
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    weather_description: str
    wind_speed: float
    wind_deg: int


class WeatherDataCreate(WeatherDataBase):
    pass


class WeatherData(WeatherDataBase):
    id: int
    class Config:
        from_attributes = True