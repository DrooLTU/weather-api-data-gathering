import httpx
import os
import sys
import concurrent.futures
import argparse
from dotenv import load_dotenv

# Add the parent directory (project root) to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from data import cities

# Load environment variables from .env file
load_dotenv()

# API endpoint URL
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather_data(lat: int, lon: int):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"{API_BASE_URL}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses
            return response.json()
    except Exception as e:
        print(f"An error occurred while fetching weather data for lat={lat}, lon={lon}: {e}")
        return None  # Return None to handle this error case
    

def process_data(executor):
    future_to_city = {
        executor.submit(fetch_weather_data, city["lat"], city["lon"]): city
        for city in cities.cities
    }
    for future in concurrent.futures.as_completed(future_to_city):
        city = future_to_city[future]
        try:
            weather_data = future.result()
            if weather_data:
                print(f"Weather data for {city['city']}:")
                # print(weather_data)
                print(cities.transform_city_data(weather_data))
                print("------")
        except Exception as e:
            print(f"Error occurred while processing weather data for {city['city']}: {e}")


def do_thread_pool():
    with concurrent.futures.ThreadPoolExecutor() as executor:
       process_data(executor)

def do_process_pool():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_data(executor)


def main():
    """
    Select which parallelism to use with the -t and -p options.
    Default is thread pool.
    """
    parser = argparse.ArgumentParser(description="Script with -t and -p options")

    parser.add_argument("-t", "--thread", action="store_true", help="Run the thread pool")
    parser.add_argument("-p", "--process", action="store_true", help="Run the process pool")

    args = parser.parse_args()

    if args.process:
        do_thread_pool()
    else:
        do_thread_pool()


if __name__ == "__main__":
    main()
