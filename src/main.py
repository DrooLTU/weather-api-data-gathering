import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
project_src = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_src)

from data.db import SessionLocal, Base, engine

from data.schemas.city_schema import City, CityCreate
from data.schemas.weather_data_schema import WeatherData, WeatherDataCreate

import data.models.table_views_model as Views

from crud.city_crud import create_city, get_cities
from crud.weather_data_crud import create_weather_data, get_weather_data, get_weather_data_index


from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/cities/", response_model=list[City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)) -> list[City]:
    """
    Get city records from the database.

    Parameters:
    -----------
    skip : int, optional
        The number of records to skip. Defaults to 0.

    limit : int, optional
        The maximum number of records to return. Defaults to 100.
    
    db : Session, optional
        The SQLAlchemy database session. If not provided, it will be obtained from
        the dependency injection system.

    Returns:
    --------
    list[City]
        A list of city records represented by the City schema.

    Raises:
    -------
    HTTPException
        If the city retrieval fails due to a database error.

    Example:
    --------
    To get all city records, make a GET request to /cities/. The response will
    contain a list of city records in the City format.

    To get the first 10 city records, make a GET request to /cities/?limit=10.
    """
    cities = get_cities(db, skip=skip, limit=limit)
    return cities


@app.post("/cities/", status_code=201)
def create_city_route(
    city_data: CityCreate,
    db_session: Session = Depends(get_db_session)
) -> City:
    """
    Create a new city record in the database.

    Parameters:
    -----------
    city_data : CityCreate
        The data for the new city to be created. Must conform to the CityCreate.

    db_session : Session, optional
        The SQLAlchemy database session. If not provided, it will be obtained from
        the dependency injection system.

    Returns:
    --------
    City
        The newly created city data represented by the City schema.

    Raises:
    -------
    HTTPException
        - If the city creation fails due to a database error.
        - If the input data does not conform to the CityCreateSchema.

    Example:
    --------
    To create a new city, make a POST request to /cities/ with the JSON data in the
    request body conforming to the CityCreateSchema. The response will contain the
    created city data in the CityCreate format.
    """
    new_city = create_city(db_session, city_data)

    if not new_city:
        raise HTTPException(status_code=500, detail="City creation failed. Please try again later.")

    return new_city


#WEATHER DATA ROUTES

@app.get("/weather_data/", response_model=list[WeatherData])
def read_weather_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)) -> list[WeatherData]:
    """
    Get weather data records from the database.

    Parameters:
    -----------
    skip : int, optional
        The number of records to skip. Defaults to 0.

    limit : int, optional
        The maximum number of records to return. Defaults to 100.

    db : Session, optional
        The SQLAlchemy database session. If not provided, it will be obtained from
        the dependency injection system.

    Returns:
    --------
    list[WeatherData]
        A list of weather data records represented by the WeatherData schema.

    Raises:
    -------
    HTTPException
        If the weather data retrieval fails due to a database error.

    Example:
    --------
    To get all weather data records, make a GET request to /weather_data/. The response will
    contain a list of weather data records in the WeatherData format.

    To get the first 10 weather data records, make a GET request to /weather_data/?limit=10.
    """
    weather_data = get_weather_data_index(db, skip=skip, limit=limit)
    return weather_data


@app.post("/weather_data/", status_code=201)
def create_weather_data_route(
    weather_data: WeatherDataCreate,
    db_session: Session = Depends(get_db_session)
) -> WeatherData:
    """
    Create a new weather data record in the database.

    Parameters:
    -----------
    weather_data : WeatherDataCreate
        The data for the new weather data to be created. Must conform to the WeatherDataCreate.

    db_session : Session, optional
        The SQLAlchemy database session. If not provided, it will be obtained from
        the dependency injection system.

    Returns:
    --------
    WeatherData
        The newly created weather data represented by the WeatherData schema.

    Raises:
    -------
    HTTPException
        - If the weather data creation fails due to a database error.
        - If the input data does not conform to the WeatherDataCreateSchema.

    Example:
    --------
    To create a new weather data, make a POST request to /weather_data/ with the JSON data in the
    request body conforming to the WeatherDataCreateSchema. The response will contain the
    created weather data in the WeatherDataCreate format.
    """
    new_weather_data = create_weather_data(db_session, weather_data)

    if not new_weather_data:
        raise HTTPException(status_code=500, detail="Weather data creation failed. Please try again later.")

    return new_weather_data


@app.get("/views/times-rained-yesterday/")
def get_times_rained_yesterday_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the times_rained_yesterday view
    """
    view_data = db.query(Views.TimesRainedYesterday).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/times-rained-last-week/")
def get_times_rained_last_week_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the times_rained_last_week view
    """
    view_data = db.query(Views.TimesRainedLastWeek).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-per-hour/")
def get_temp_per_hour_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_temp_per_hour view
    """
    view_data = db.query(Views.TempPerHour).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-per-day/")
def get_temp_per_day_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_temp_per_day view
    """
    view_data = db.query(Views.TempPerDay).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-per-week/")
def get_temp_per_week_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_temp_per_week view
    """
    view_data = db.query(Views.TempPerWeek).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-today/")
def get_temp_today_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_stddev_temp_today view
    """
    view_data = db.query(Views.TempToday).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-yesterday/")
def get_temp_yesterday_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_stddev_temp_yesterday view
    """
    view_data = db.query(Views.TempYesterday).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-current-week/")
def get_temp_current_week_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_stddev_temp_current_week view
    """
    view_data = db.query(Views.TempCurrentWeek).offset(offset).limit(limit).all()
    return view_data


@app.get("/views/temp-last-seven-days/")
def get_temp_last_seven_days_data(offset: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """
    Get the data from the max_min_stddev_temp_last_seven_days view
    """
    view_data = db.query(Views.TempLastSevenDays).offset(offset).limit(limit).all()
    return view_data