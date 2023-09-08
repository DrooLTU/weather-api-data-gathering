from pydantic import BaseModel, Field

class CityBase(BaseModel):
    city: str = Field(..., example="New York")
    country: str = Field(..., example="United States")
    lat: float = Field(..., example=40.7128)
    lon: float = Field(..., example=-74.0060)


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    class Config:
        from_attributes = True

