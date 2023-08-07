import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from fetch import fetch_coroutine
from data.db import SessionLocal

from data.schemas.city_schema import CitySchema, CityCreateSchema
from crud.city_crud import create_city

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=CitySchema, status_code=201)
def create_city_route(
    city_data: CityCreateSchema,
    db: Session = Depends(get_db)
) -> CitySchema:
    """
    Create a new city record in the database.

    Parameters:
    -----------
    city_data : CityCreateSchema
        The data for the new city to be created. Must conform to the CityCreateSchema.

    db : Session, optional
        The SQLAlchemy database session. If not provided, it will be obtained from
        the dependency injection system.

    Returns:
    --------
    CitySchema
        The newly created city data represented by the CitySchema.

    Raises:
    -------
    HTTPException
        - If the city creation fails due to a database error.
        - If the input data does not conform to the CityCreateSchema.

    Example:
    --------
    To create a new city, make a POST request to /cities/ with the JSON data in the
    request body conforming to the CityCreateSchema. The response will contain the
    created city data in the CitySchema format.
    """
    new_city = create_city(db, city_data)

    if not new_city:
        raise HTTPException(status_code=500, detail="City creation failed. Please try again later.")

    return new_city





# if __name__ == "__main__":
#     fetch_coroutine.main()