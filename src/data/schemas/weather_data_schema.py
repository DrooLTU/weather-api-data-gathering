from pydantic import BaseModel

class WeatherDataCreateSchema(BaseModel):
    city_id: int
    temperature: float
    humidity: int
    wind_speed: float

    class Config:
        schema_extra = {
            "example": {
                "city_id": "1",
                "temperature": 23.5,
                "humidity": 90,
                "wind_speed": 5.2
            }
        }


class WeatherDataSchema(WeatherDataCreateSchema):
    id: int

    class Config:
        from_attributes = True