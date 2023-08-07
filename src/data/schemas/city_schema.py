from pydantic import BaseModel

class CitySchema(BaseModel):
    city: str
    country: str
    lat: float
    lon: float

    class Config:
        from_attributes = True

class CityCreateSchema(BaseModel):
    title: str
    country: str
    lat: float
    lon: float

    class Config:
        schema_extra = {
            "example": {
                "title": "New York",
                "country": "United States",
                "lat": 40.7128,
                "lon": -74.0060
            }
        }