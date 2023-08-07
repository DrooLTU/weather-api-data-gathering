from pydantic import BaseModel

class WeatherDataSchema(BaseModel):
    city_id: int
    temperature: float
    humidity: int
    wind_speed: float

    class Config:
        from_attributes = True