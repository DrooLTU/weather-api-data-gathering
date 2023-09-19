import aiohttp
import asyncio
import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import pandas as pd
from data.db import engine
from data.cities import transform_city_data

load_dotenv()

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def put_data(df: pd.DataFrame):
    table_name = 'weather_data'
    df.to_sql(table_name, engine, if_exists='append', index=False)
    engine.dispose()

def get_cities()-> pd.DataFrame:
    query = 'SELECT * FROM cities'
    return pd.read_sql(query, engine)

async def fetch_weather_data(session: aiohttp.ClientSession, city: pd.Series) -> list:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"{API_BASE_URL}?lat={city['lat']}&lon={city['lon']}&appid={api_key}&units=metric"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            response = await response.json()
            transformed_data = transform_city_data(response, city)
            put_data(transformed_data)
            return transformed_data
    except asyncio.TimeoutError:
        print(f"Timeout error occurred while fetching weather data for city {city['name']}.")
        return None
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching weather data for city {city['name']}: {e}")
        return None

async def process_data(cities: pd.DataFrame):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather_data(session, city) for index, city in cities.iterrows()]
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError as e:
            print("One or more errors occurred while fetching weather data.")
            return


async def main():
    cities = get_cities()
    await process_data(cities)


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    """
    This is needed to fix an issue on Windows machines to stop throwing 'loop closed' exception
    """
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    asyncio.run(main())