import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from typing import List, Optional

from sqlalchemy.orm import relationship, Mapped, mapped_column
from db import Base

from models.weather_data_model import WeatherData

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    weather_data: Mapped[Optional[List["WeatherData"]]] = relationship(back_populates='city')
