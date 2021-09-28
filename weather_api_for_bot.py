import requests
from datetime import datetime
from cred import Creds

weather_api_key = Creds.weather_api_key


def by_coordinate(lat, lon):
    r = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric"
            .format(lat, lon, weather_api_key))
    r = r.json()
    # pprint(r)
    date = datetime.fromtimestamp(r["dt"])
    country = r["sys"]["country"]
    city = r["name"]
    weather_summary = r["weather"][0]["main"]
    weather_description = r["weather"][0]["description"]
    temp = r["main"]["temp"]
    temp_realfeel = r["main"]["feels_like"]
    cloudiness = r["clouds"]["all"]
    humidity = r["main"]["humidity"]
    temp_max = r["main"]["temp_max"]
    temp_min = r["main"]["temp_min"]
    weather_icon = r["weather"][0]["icon"]
    weather_icon_url = "http://openweathermap.org/img/wn/{}@4x.png".format(weather_icon)

    return f'{date}\n' \
           f'Country     :    {country}\n' \
           f'City        :    {city}\n' \
           f'Weather     :    {weather_summary}\n' \
           f'Details     :    {weather_description}\n' \
           f'Temperature :    {temp} °C\n' \
           f'RealFeel    :    {temp_realfeel} °C\n' \
           f'Max Temp    :    {temp_max} °C\n' \
           f'Min Temp    :    {temp_min} °C\n' \
           f'Cloudiness  :    {cloudiness} %\n' \
           f'Humidity    :    {humidity} %', weather_icon_url
