import pandas as pd

"""
Here goes cities with lat, long.
"""

cities = [
    {"city": "Istanbul", "country": "Turkey", "lat": 41.0082, "lon": 28.9784},
    {"city": "London", "country": "United Kingdom", "lat": 51.5074, "lon": -0.1278},
    {"city": "Saint Petersburg", "country": "Russia", "lat": 59.9343, "lon": 30.3351},
    {"city": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"city": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
    {"city": "Kyiv", "country": "Ukraine", "lat": 50.4501, "lon": 30.5234},
    {"city": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"city": "Bucharest", "country": "Romania", "lat": 44.4268, "lon": 26.1025},
    {"city": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"city": "Minsk", "country": "Belarus", "lat": 53.9045, "lon": 27.5615},
    {"city": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"city": "Warsaw", "country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"city": "Hamburg", "country": "Germany", "lat": 53.5511, "lon": 9.9937},
    {"city": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402},
    {"city": "Belgrade", "country": "Serbia", "lat": 44.7866, "lon": 20.4489},
    {"city": "Barcelona", "country": "Spain", "lat": 41.3851, "lon": 2.1734},
    {"city": "Munich", "country": "Germany", "lat": 48.1351, "lon": 11.5820},
    {"city": "Kharkiv", "country": "Ukraine", "lat": 49.9935, "lon": 36.2304},
    {"city": "Milan", "country": "Italy", "lat": 45.4642, "lon": 9.1900}
]


def transform_city_data(data: tuple) -> pd.DataFrame:

    weather_data = []

    
    dt = data['dt']
    human_timestamp = pd.to_datetime(data['dt'], unit='s')
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    weather_description = data['weather'][0]['description']
    wind_speed = data['wind']['speed']
    wind_deg = data['wind']['deg']


    weather_data.append({
        'DateTime': dt, 'Readable_Date': human_timestamp, 'Temperature': temp, 'Feels_Like': feels_like, 'Temp_Min': temp_min,
        'Temp_Max': temp_max, 'Pressure': pressure, 'Humidity': humidity,
        'Weather_Description': weather_description, 'Wind_Speed': wind_speed, 'Wind_Deg': wind_deg,
    })

    weather_df = pd.DataFrame(weather_data)
    return weather_df


