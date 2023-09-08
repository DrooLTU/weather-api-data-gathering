from pydantic import BaseModel

class WeatherDataBase(BaseModel):
    city_id: int
    temperature: float
    humidity: int
    wind_speed: float


class WeatherDataCreate(WeatherDataBase):
    pass


class WeatherData(WeatherDataBase):
    id: int
    class Config:
        from_attributes = True