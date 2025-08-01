import requests


class Weather:
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude
        self.url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self, api):
        """
        :param api:
        :return: Dictionary containing next 3 days weather in Celsius
        """
        weather_params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': api,
        }

        weather_res = requests.get(self.url, weather_params)
        weather_res.raise_for_status()
        weather_data = weather_res.json()

        weather = {}
        for _ in range(3):
            weather[f"Day {_ + 1}"] = {
                "Temperature": f"{round(weather_data['list'][_]['main']['temp'] - 273, 2)} °C",
                "Weather": weather_data["list"][_]["weather"][0]["description"]
            }

        return weather
