import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db import Base

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'))
    city: Mapped["City"] = relationship(back_populates='weather_data')
    temperature: Mapped[float] = mapped_column()
    humidity: Mapped[int] = mapped_column()
    wind_speed: Mapped[float] = mapped_column()

