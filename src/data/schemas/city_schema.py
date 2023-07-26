from pydantic import BaseModel

class CitySchema(BaseModel):
    city: str
    country: str
    lat: float
    lon: float