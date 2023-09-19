import os
import sys
from sqlalchemy import Column, Integer, Float, String

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from db import Base


class TimesRainedYesterday(Base):
    __tablename__ = "times_rained_yesterday"
    times_rained = Column(Integer, primary_key=True)

class TimesRainedLastWeek(Base):
    __tablename__ = "times_rained_last_week"
    times_rained = Column(Integer, primary_key=True)

class BaseMinMax():
    max_temperature = Column(Float, primary_key=True)
    min_temperature = Column(Float, primary_key=True)
    max_temp_city_name = Column(String(255), primary_key=True)
    min_temp_city_name = Column(String(255), primary_key=True)


class TempPerHour(BaseMinMax, Base):
    __tablename__ = "max_min_temp_per_hour"
    hour = Column(Integer, primary_key=True)

class TempPerDay(BaseMinMax, Base):
    __tablename__ = "max_min_temp_per_day"
    date = Column(String(255), primary_key=True)

class TempPerWeek(BaseMinMax, Base):
    __tablename__ = "max_min_temp_per_week"
    week = Column(Integer, primary_key=True)


class BaseStdDev():
    country = Column(String(255), primary_key=True)
    city = Column(String(255), primary_key=True)

class TempToday(BaseStdDev, Base):
    __tablename__ = "max_min_stddev_temp_today"
    max_temperature_today = Column(Float, primary_key=True)
    min_temperature_today = Column(Float, primary_key=True)
    stddev_temperature_today = Column(Float, primary_key=True)

class TempYesterday(BaseStdDev, Base):
    __tablename__ = "max_min_stddev_temp_yesterday"
    max_temperature_yesterday = Column(Float, primary_key=True)
    min_temperature_yesterday = Column(Float, primary_key=True)
    stddev_temperature_yesterday = Column(Float, primary_key=True)

class TempCurrentWeek(BaseStdDev, Base):
    __tablename__ = "max_min_stddev_temp_current_week"
    max_temperature_current_week = Column(Float, primary_key=True)
    min_temperature_current_week = Column(Float, primary_key=True)
    stddev_temperature_current_week = Column(Float, primary_key=True)

class TempLastSevenDays(BaseStdDev, Base):
    __tablename__ = "max_min_stddev_temp_last_seven_days"
    max_temperature_last_seven_days = Column(Float, primary_key=True)
    min_temperature_last_seven_days = Column(Float, primary_key=True)
    stddev_temperature_last_seven_days = Column(Float, primary_key=True)