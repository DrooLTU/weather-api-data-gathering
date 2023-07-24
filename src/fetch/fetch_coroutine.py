import aiohttp
import asyncio
import os
import sys
from dotenv import load_dotenv
# Add the parent directory (project root) to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from data import cities

# Load environment variables from .env file
load_dotenv()

# API endpoint URL
API_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


async def fetch_weather_data(session: aiohttp.ClientSession, lat: int, lon: int) -> list:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"{API_BASE_URL}?lat={lat}&lon={lon}&appid={api_key}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise exception for non-2xx responses
            return await response.json()
    except asyncio.TimeoutError:
        print(f"Timeout error occurred while fetching weather data for lat={lat}, lon={lon}.")
        return None  # Return None to handle this error case
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching weather data for lat={lat}, lon={lon}: {e}")
        return None  # Return None to handle this error case

async def process_data():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather_data(session, city["lat"], city["lon"]) for city in cities.cities]
        try:
            weather_data = await asyncio.gather(*tasks)
        except asyncio.CancelledError as e:
            print("One or more errors occurred while fetching weather data.")
            return
        for i, city in enumerate(cities.cities):
            print(f"Weather data for {city['city']}:")
            print(cities.transform_city_data(weather_data[i]))
            print("------")
            pass

async def main():
    await process_data()


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    """
    This is needed to fix an issue on Windows machines to stop throwing 'loop closed' exception
    """
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    asyncio.run(main())