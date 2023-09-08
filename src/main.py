import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


from fetch import fetch_coroutine
from data.db import SessionLocal, Base, engine
from data.schemas.city_schema import City, CityCreate
from crud.city_crud import create_city, get_cities


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
        The newly created city data represented by the City model.

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





# if __name__ == "__main__":
#     fetch_coroutine.main()