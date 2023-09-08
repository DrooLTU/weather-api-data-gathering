import httpx
import os
import sys
import concurrent.futures
import argparse
from dotenv import load_dotenv

# Add the parent directory (project root) to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import pandas as pd
from data.db import engine
from data.cities import transform_city_data

# Load environment variables from .env file
load_dotenv()

# API endpoint URL
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def put_data(df: pd.DataFrame):
    table_name = 'weather_data'
    df.to_sql(table_name, engine, if_exists='append', index=False)
    engine.dispose()

def get_cities()-> pd.DataFrame:
    query = 'SELECT * FROM cities'
    return pd.read_sql(query, engine)


def fetch_weather_data(city: pd.Series):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"{API_BASE_URL}?lat={city['lat']}&lon={city['lon']}&appid={api_key}&units=metric"
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses
            response = response.json()
            transformed_data = transform_city_data(response, city)
            put_data(transformed_data)
            return transformed_data
    except Exception as e:
        print(f"An error occurred while fetching weather data for city {city['name']}: {e}")
        return None 
    

def process_data(cities: pd.DataFrame, executor: concurrent.futures.Executor):
    future_to_city = {
        executor.submit(fetch_weather_data, city): city
        for index, city in cities.iterrows()
    }
    for future in concurrent.futures.as_completed(future_to_city):
        city = future_to_city[future]
        try:
            future.result()
        except Exception as e:
            print(f"Error occurred while processing weather data for {city['city']}: {e}")


def do_thread_pool(cities: pd.DataFrame):
    with concurrent.futures.ThreadPoolExecutor() as executor:
       process_data(cities, executor)

def do_process_pool(cities: pd.DataFrame):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_data(cities, executor)


def main():
    """
    Select which parallelism to use with the -t and -p options.
    Default is thread pool.
    """
    parser = argparse.ArgumentParser(description="Script with -t and -p options")

    parser.add_argument("-t", "--thread", action="store_true", help="Run the thread pool")
    parser.add_argument("-p", "--process", action="store_true", help="Run the process pool")

    args = parser.parse_args()

    cities = get_cities()

    if args.process:
        do_thread_pool(cities)
    else:
        do_thread_pool(cities)


if __name__ == "__main__":
    main()
